#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys  
import os
import traceback
import smtplib
from email.mime.text import MIMEText
  
mail_host = '' #发送邮件的smtp地址  
mail_user = '' # 发送通知邮件的用户名  
mail_pass = '' # 用户的密码  
me = 'SVN Service'+'<'+'des'+'@'+'has'+'>' #发送邮件人的地址标识  
to_list = ['zhao'] # 收件人  

reload(sys)
sys.setdefaultencoding('utf-8')

html_template = """ 
<html> 
        <h2 style="color:#FFFFFF; background: #008040;">基本信息</h2> 
        <div> <b>版本库：</b> 
                <a href="svn:%s">%s</a> 
        </div> 
        <div> <b>版本号：</b>%s 
        </div> 
        <div> 
                <b>提交者：</b>%s 
        </div> 
        <div> 
                <b>提交时间：</b>%s 
        </div> 
        <h2 style="color:#FFFFFF; background: #4682B4;">提交说明</h2> <font size="4" color="#BF6000"><xmp>%s</xmp></font> 
        <h2 style="color:#FFFFFF; background: #5353A8;">文件清单</h2> 
        <xmp>%s</xmp> 
	<a href="http://www.baidu.com" style="display:block;background-color:DodgerBlue;">代码修改详情</a>
        <style type="text/css"> 
                a:link,a:visited{font-size:20px} 
                a:hover,a:active{font-size:22px}
        </style>
        <hr> 
        <center> 
                ☆ Powered by: zyb
        </center> 
</html> 
"""  
  
def get_repo_name(repo):  
        return os.path.basename(repo)  
  
def get_author(repo, rev):  
        """svnlook author -r REV REPOS 获得提交者 
        """  
        cmd = '%s author -r %s %s' % (svnlook_bin_path, rev, repo)  
        output = os.popen(cmd).read()  
        return output  
  
def get_date(repo, rev):  
        """svnlook date -r REV REPOS 获得提交时间 
        """  
        cmd = '%s date -r %s %s' % (svnlook_bin_path, rev, repo)  
        output = os.popen(cmd).read()  
        return output  
  
def get_log(repo, rev):  
        """svnlook log -r REV REPOS 获得提交日志 
        """  
        cmd = '%s log -r %s %s' % (svnlook_bin_path, rev, repo)  
        output = os.popen(cmd).read()  
        return output
  
def get_file_list(repo, rev):  
        """svnlook changed -r REV REPOS 获得发生变更的文件 
        """  
        cmd = '%s changed -r %s %s' % (svnlook_bin_path, rev, repo)  
        output = os.popen(cmd).read()  
        return output

def get_diff_dir(repo, rev):
	"""svnlook diff -r REV REPOS 获得发生变更的文件内容
        """
        cmd = '%s diff -r %s %s' % (svnlook_bin_path, rev, repo)
        output = os.popen(cmd).read()
        return output
  
def send_mail(me, to_list, msg):  
        try:  
                s = smtplib.SMTP()  
                s.connect(mail_host)  
                s.login(mail_user,mail_pass)  
                s.sendmail(me, to_list, msg.as_string())  
                s.close()  
                return True  
        except Exception, e:  
		print traceback.format_exc() 
                return False  
  
def write_mail(me, to_list, sub, content):
        msg = MIMEText(content,_subtype='html',_charset='utf-8')  
        msg['Subject'] = sub
        msg['From'] = me  
        msg['To'] = ';'.join(to_list)  
        msg["Accept-Language"]="zh-CN"  
        msg["Accept-Charset"]="ISO-8859-1,utf-8"
        return msg  
  
global svnlook_bin_path  
  
def write_mail_content(repo, rev):  
        """ 
        repo: repository 
        rev: revision 
        """  
        repo_name = get_repo_name(repo)  
        author = get_author(repo, rev)  
        date = get_date(repo, rev)  
        log = get_log(repo, rev)
        file_list = get_file_list(repo, rev)  
        content = html_template % (repo, repo_name, rev, author, date, log, file_list)  
        return content
  
if __name__ == '__main__':  
        svnlook_bin_path = '/usr/bin/svnlook'  
        subject = 'SVN Commit Notification'  
        content = write_mail_content(sys.argv[1], sys.argv[2])
        msg = write_mail(me, to_list, subject, content)
        send_mail(me, to_list, msg)
