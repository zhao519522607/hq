#! /usr/bin/env python
# -*- coding: utf-8 -*- 
import oss2,sys
import smtplib  
from email.mime.text import MIMEText

mailto_list = ["aa"]
mail_host = "smtp.exmail.qq.com"
mail_user = "bb"
mail_pass = ""
oss2.defaults.connection_pool_size = 6
auth = oss2.Auth('', '')
bucket = oss2.Bucket(auth, 'http://osaaa', 'bb')

def send_mail(to_list,sub,content):  
    me="oss_error"+"<"+mail_user+">"  
    msg = MIMEText(content,_subtype='plain',_charset='gb2312')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True  
    except Exception, e:  
        print str(e)  
        return False 

def upload(file):
    try:
        with open(file,'r+') as f:
              lines = f.readlines()
              for line in lines:
            	       line1 = line.strip('\n')
            	       remote_file = line1.split('/data1/')
		       oss2.resumable_upload(bucket, remote_file[1], line1,
    		                  store=oss2.ResumableStore(root='/tmp'),
    		                  multipart_threshold=100*1024,
    			          part_size=100*1024,
    				  num_threads=4)
		       with open(line1, 'rb') as fileobj:
			     assert bucket.get_object(remote_file[1]).read() == fileobj.read(), "%s upload oss failed!" %line1
    except Exception,e:
        #print "There is an error please check."
	send_mail(mailto_list,"oss error","mysql upload oss fault,%s!" %e)

if __name__ == '__main__':
	file_name = sys.argv[1]
	upload(file_name)
