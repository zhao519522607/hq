#! /usr/bin/env python
# -*- coding: utf-8 -*- 
import oss2,sys,time
import smtplib
import traceback
import optparse
from email.mime.text import MIMEText

mailto_list = [""]
mail_host = "smtp"
mail_user = ""
mail_pass = ""
oss2.defaults.connection_pool_size = 6
auth = oss2.Auth('', '')
bucket = oss2.Bucket(auth, 'http://', '')

class oper_oss(object):

        def send_mail(self,to_list,sub,content):
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
                except:
                        #print "except in send_mail:%s" % traceback.format_exc()  
                        return False

        def upload(self,file):
                with open(file,'r+') as f:
                        lines = f.readlines()
                        for line in lines:
                                line1 = line.strip('\n')
                                remote_file = line1.split('/data1/jenkins_dir/')
                                oss2.resumable_upload(bucket, remote_file[1], line1,
                                        store=oss2.ResumableStore(root='/tmp'),
                                        multipart_threshold=100*1024,
                                        part_size=100*1024,
                                        num_threads=4)
                        #with open(line1, 'rb') as fileobj:
                             #assert bucket.get_object(remote_file[1]).read() == fileobj.read(), "%s upload oss failed!" %line1

        def download(self,url):
                if bucket.object_exists(url):
                        local_f = "/data1/jenkins_dir/" + url
                        oss2.resumable_download(bucket, url, local_f,
                                store=oss2.ResumableDownloadStore(root='/tmp'),
                                multiget_threshold=20*1024*1024,
                                part_size=10*1024*1024,
                                num_threads=2)
                        return True
                else:
                        return False

def option_parser():
        try:
                parser = optparse.OptionParser("python oper_oss.py -h |For Example: python oper_oss.py -m upload -f file || python oper_oss.py -m download -f package/fxapi/test2")
                parser.add_option('-m', action='store', dest='mode',
                          default='download', help=(u'选择要执行的操作:1.upload(上传操作).2.download(下载操作)'))
                parser.add_option('-f', action='store', dest='file',
                          default='', help=(u'需要上传的文件列表文件或者需要下载的文件路径'))
                return parser
        except:
                print("Failed to create option parser: %s" %traceback.format_exc())
                return None

if __name__ == '__main__':
        opt_parser = option_parser()
        if len(sys.argv) == 1:
                opt_parser.print_help()
                sys.exit(1)

        (options, args) = opt_parser.parse_args(sys.argv)
        _oss = oper_oss()

        if options.mode == "upload":
                try:
                        _oss.upload(options.file)
                except Exception,e:
                        _oss.send_mail(mailto_list,'oss error','jenkins upload oss fault,%s!' %e)
                        time.sleep(5)
                        _oss.upload(options.file)
        elif options.mode == "download":
                try:
                        _oss.download(options.file)
                except Exception,e:
                        _oss.send_mail(mailto_list,'oss error','jenkins download oss fault,%s!' %e)
                        time.sleep(5)
                        _oss.download(options.file)
        else:
                print "illegal mode:%s" % options.mode
