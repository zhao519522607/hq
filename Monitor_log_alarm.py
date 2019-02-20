#! /usr/bin/env python
# -*- coding: utf8 -*-
#Author: zyb

from kafka import KafkaConsumer
import traceback
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from datetime import datetime, date, timedelta

mail_host = "smtp_sever"
mailto = ["mail"]
mail_user = "user"
mail_pass = "password"
yesterday = (date.today() + timedelta(days = -1)).strftime("%Y-%m-%d")
filename = yesterday + "_error.log"

def send_mail(to_list,sub):
    try:
        me="ERROR_LOG"+"<"+mail_user+">"
        message = MIMEMultipart()
        message['From'] = Header("OPERATION", 'utf-8')
        message['To'] = ";".join(to_list)
        message['Subject'] = Header(sub, 'utf-8')
        message.attach(MIMEText('ERROR LOG MONITOR', 'plain', 'utf-8'))
        att1 = MIMEText(open('/data2/all_error_logs/%s' %filename, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="error.log"'
        message.attach(att1)
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user,mail_pass)
        server.sendmail(me, to_list, message.as_string())
        server.close()
        print "邮件发送成功"
    except:
        print "Except Error in send_mail:%s" % traceback.format_exc()

def get_messages():
    try:
        consumer = KafkaConsumer('Monitor_Log_Traceback', bootstrap_servers=['kafka_server'], group_id='Monitor_Log_G1', client_id='Monitor_Log', auto_offset_reset='earliest', consumer_timeout_ms=120000)
        for message in consumer:
            with open('/data2/all_error_logs/%s' %filename,'a+') as f:
                f.write(message.value)
    except:
        print "Except Error in get_messages:%s" % traceback.format_exc()

def main():
    try:
        get_messages()
        send_mail(mailto,"机器错误日志监控")
    except:
        print "Except Error in main:%s" % traceback.format_exc()

if __name__ == '__main__':
    try:
        main()
    except:
        print "Except Error:%s" % traceback.format_exc()
