#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zookeeper
import redis
import time
import sys
import traceback
import smtplib
import json
from collections import Counter
from operator import itemgetter, attrgetter
from email.mime.text import MIMEText

ser_list = []
content_dict = {}
mail_host = 'smtp.exmail.qq.com'
mail_user = 'develop'
mail_pass = '123445555'
me = 'Cache Codis Slowlog Notification'+'<'+'devele'+'@'+'haoqiao.cn'+'>'
mail_to_list = ['aaa','bbb']

def get_host_list():
    try:
	handler = zookeeper.init("1.1.1.1,2.2.2.2")
        data = zookeeper.get_children(handler,"/codis3/hq_cache/group")
        for i in data:
                i_s = zookeeper.get(handler,"/codis3/hq_cache/group/%s" %i)[0]
                i_list = json.loads(i_s)['servers'][0]['server']
                ser_list.append(i_list)
        zookeeper.close(handler)
    except:
        print "except in get_host_list:%s" % traceback.format_exc()
        
def codis_command():
    try:
        for s in ser_list:
            s_tmp = s.split(':')
            r = redis.Redis(host=s_tmp[0], port=int(s_tmp[1]))
            result = r.slowlog_get(200)
	    content_dict[s_tmp[0]] = result
	    r.slowlog_reset()
    except:
        print "except in codis_command:%s" % traceback.format_exc()

def output_common_data(title, header_list, common_data_list):
        tail_info = '''</div>
           </span>
           </script>
           </body>
        </html>'''
        out_str = '''<html>
        <head>
            <meta charset="gbk">
            <title>%s</title>
            <style type="text/css">
            .font12px{font-family:Verdana, Geneva, sans-serif; font-size:12px;}
            #data{border-collapse:collapse; border:1px solid #EEE; margin:0 auto;}
            #data th{background:#EEE; border-bottom:1px solid #CCC; padding:4px; text-align:left;}
            #data td{border:1px solid #EEE; padding:4px;}
            tr:nth-child(even) {background: #CCC}
            tr:nth-child(odd) {background: #FFF}
            </style>
        </head>
        <body onload="linecolor();">
            <div>
            <span>
            <div class="url_list">
                <table class="font12px" border="1" id="data">
        '''%(title)
        out_str += '<tr>'
        for header in header_list:
            out_str += '<th>%s</th>'%(header)
        out_str += '</tr>'
        
        for common_data in common_data_list:
            out_str += '<tr>\n'
            for data in common_data:
                if isinstance(data, unicode):
                    out_str += '<td>' + data + '</td>\n'
                else:
                    out_str += '<td>' + str(data) + '</td>\n'
            out_str += '</tr>\n'
        out_str += tail_info
        return out_str

def compute_command(host, infos):
    try:
        if not infos:
            return []
        data_list = []
        parameter_len = 5
        for info in infos:
            duration = info['duration']
            start_time = info['start_time']
            command_string = info['command']
            command = command_string.split(' ')[0]
	    try:
            	key = command_string.split(' ')[1]
            	parameters = ' '.join(command_string.split(' ')[1:])
	    except:
		continue
            param_list = key.split(':')[:parameter_len]
            param_len_list = []
            param_len_list.append(command + ' ' + key)
            for i in range(parameter_len, 0, -1):
               param_len_list.append(command + ' ' + ':'.join(param_list[0:i]))
            param_len_list.append(duration)
            data_list.append(param_len_list)
    except:
       print traceback.format_exc()
    
    param_compute_dict = {}
    for i in range(10, 1, -1):
        for param_len_list in data_list:
            if len(param_len_list) == i:
                if i in param_compute_dict:
                    param_compute_dict[i].append(param_len_list)
                else:
                    param_compute_dict[i] = [param_len_list]
    result_dict = {}
    for count, params_list in param_compute_dict.items():
        map_list = zip(*params_list)
        for i in range(0, len(map_list) -1):
            info = map_list[i]
            for (key,num) in Counter(info).most_common():
                if num > 1 and key not in result_dict:
                    result_dict[key] = num
    #print json.dumps(result_dict,indent=4)
    
    remove_key_list = []
    for key in result_dict.keys():
        count = 0
        for compare_key in result_dict.keys():
            if compare_key.startswith(key):
                count += 1
        if count > 1:
            remove_key_list.append(key)
    for key in remove_key_list:
        del result_dict[key]
    #print json.dumps(result_dict,indent=4) 
    
    final_result = []
    for last_command, count in Counter(result_dict).most_common():
        use_time_list = []
        for count1, params_list in param_compute_dict.items():
            for params in params_list:
                for param in params[:-1]:
                    if param.startswith(last_command):
                        use_time = params[len(params)-1]
                        use_time_list.append(use_time)
                        break
        avg_use_time = reduce(lambda x,y:x+y ,use_time_list) / len(use_time_list)
        final_result.append([host, last_command, count, avg_use_time])
    
    final_result = sorted(final_result,key=itemgetter(2,3), reverse=True)
    return final_result
    
def pretty_table(dictionary):
    try:
        format_infos = []
        for host, infos in dictionary.items():
            format_info = compute_command(host, infos)
	    if not format_info:
                continue
            format_infos.extend(format_info)
        format_infos = sorted(format_infos,key=itemgetter(2,3), reverse=True)
        html = output_common_data(u'集群统计', [u'主机名', u'命令', u'次数', u'时长'], format_infos)
        return html
    except:
        print "except in pretty_table:%s" % traceback.format_exc()
        
def write_mail(to_list, sub, content):
    try:
        msg = MIMEText(content,_subtype='html',_charset='utf-8')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ';'.join(to_list)
        msg["Accept-Language"]="zh-CN"
        msg["Accept-Charset"]="ISO-8859-1,utf-8"
        return msg
    except:
        print "except in write_mail:%s" % traceback.format_exc()

def send_mail(to_list, msg):
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
    except:
        print "except in send_mail:%s" % traceback.format_exc()    

def main():
    try:
        get_host_list()
        codis_command()
	pretty_table(content_dict)
        html = pretty_table(content_dict)
        msg = write_mail(mail_to_list,"Cache Codis Slowlog",html)
        send_mail(mail_to_list,msg)
    except:
        print "except in main:%s" % traceback.format_exc()

if __name__ == '__main__':
    main()
