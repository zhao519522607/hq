#! /usr/bin/env python
# -*- coding: utf8 -*-

import traceback,datetime,sys
import optparse,json
import urllib2
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from aliyunsdkcore import client
from aliyunsdkrds.request.v20140815 import CreateDiagnosticReportRequest
from aliyunsdkrds.request.v20140815 import DescribeDiagnosticReportListRequest

reg = "区域"
download_dict = {}
mailto_basic = ["收件人"]
mailto_car = [""]
mail_host = "smtp"
mail_user = "用户"
mail_pass = "密码"
today = datetime.datetime.today().strftime("%Y-%m-%d")
stime = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
etime = datetime.datetime.today().strftime("%Y-%m-%d %H:%M")
ids = ["id1,"id2","id3","id4"]

class report(object):
	def __init__(self,are):
		self.client = client.AcsClient("","",are)

	def create_report(self,id):
		try:
			request = CreateDiagnosticReportRequest.CreateDiagnosticReportRequest()
			request.set_accept_format('json')

			request.add_query_param('DBInstanceId', id)
			request.add_query_param('StartTime', stime)
			request.add_query_param('EndTime', etime)

			response = self.client.do_action_with_exception(request)
			print response
		except:
			print "Except create_report Error:%s" % traceback.format_exc()

	def get_report_list(self,id):
		try:
			request = DescribeDiagnosticReportListRequest.DescribeDiagnosticReportListRequest()
			request.set_accept_format('json')

			request.add_query_param('DBInstanceId', id)

			response = self.client.do_action_with_exception(request)
			return response
		except:
			print "Except get_report_list Error:%s" % traceback.format_exc()

	def download_report(self,rdd):
		try:
			report_dict = json.loads(self.get_report_list(rdd))
			report_list = report_dict["ReportList"]
			if report_list and report_list[0]["DiagnosticTime"].split('T')[0] == today:
				download_dict[rdd] = report_list[0]["DownloadURL"]
		except:
			print "Except download_report Error:%s" % traceback.format_exc()

def send_mail(to_list,sub,name):
	me="RDS_Server"+"<"+mail_user+">"
	message = MIMEMultipart()
	message['From'] = Header("RDS-ADMIN", 'utf-8')
	message['To'] = ";".join(to_list)
	message['Subject'] = Header(sub, 'utf-8')
	message.attach(MIMEText('RDS实例id: %s 慢查询分析报告' %name, 'plain', 'utf-8'))
	att1 = MIMEText(open('/data1/RDSPDF/%s.pdf' %name, 'rb').read(), 'base64', 'utf-8')
	att1["Content-Type"] = 'application/octet-stream'
	att1["Content-Disposition"] = 'attachment; filename="slow-report.pdf"'
	message.attach(att1)
	try:
		server = smtplib.SMTP()
		server.connect(mail_host)
		server.login(mail_user,mail_pass)
		server.sendmail(me, to_list, message.as_string())
		server.close()
		print "邮件发送成功"
	except smtplib.SMTPException:
		print "Error: 无法发送邮件"

def option_parser():
	try:
		parser = optparse.OptionParser("python RDS-REPORT.py -h")
		parser.add_option('-c', action='store_true', dest='create',
                          default=False, help=u'create RDS report')
		parser.add_option('-g', action='store_true', dest='get',
                          default=False, help=u'get RDS report')
		return parser
	except:
		print("Failed to create option parser.")
		return None

if __name__ == '__main__':
	try:
		opt_parser = option_parser()
		if len(sys.argv) == 1:
			opt_parser.print_help()
			sys.exit(1)

		rep = report(reg)
		(options, args) = opt_parser.parse_args(sys.argv)
		if options.create:
			for rd in ids:
				rep.create_report(rd)
		elif options.get:
			for rd in ids:
				rep.download_report(rd)
			for u in download_dict:
				url = download_dict[u]
				f = urllib2.urlopen(url) 
				data = f.read() 
				with open("/data1/RDSPDF/%s.pdf" %u, 'wb') as code:   
					code.write(data)
				if u == "id1":
					send_mail(mailto_car,"b数据库慢查询分析报告",u)
				elif u == 'id2':
					send_mail(mailto_basic,"主库慢查询分析报告",u)
				elif u == 'id3':
					send_mail(mailto_basic,"从库慢查询分析报告",u)
				elif u == 'id4':
					send_mail(mailto_basic,"a数据库慢查询分析报告",u)
				else:
					pass
		else:
			print "Do nothing"
	except:
		print "Except main Error:%s" % traceback.format_exc()
