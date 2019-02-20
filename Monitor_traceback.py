#! /usr/bin/env python
# -*- coding: utf8 -*-
#Author: zyb

import os
import commands
import traceback
import socket
import fcntl
import struct
from kafka import KafkaProducer

CMD = 'find /data/logs -name "*.log*" -type f -mtime 0'
KEYS = "Traceback"
producer = KafkaProducer(bootstrap_servers=['kafka_server'], client_id='monitor_error')

def get_ip_address(ifname):
    try:
       s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
       )[20:24])
    except:
        print "Except Error in get_ip_address:%s" % traceback.format_exc()

def filesname():
    try:
        (status, output) = commands.getstatusoutput(CMD)
        if status == 0:
            files_list = output.split('\n')
        else:
            print "查找文件报错"
        return files_list
    except:
        print "Except Error in filesname:%s" % traceback.format_exc()

def search_keys():
    try:
        files = filesname()
        ip_list = get_ip_address('eth0').split('.')
        for f in files:
            if f:
                if os.path.getsize(f):
                    (status, output) = commands.getstatusoutput('egrep -A 4 -w "Traceback" %s |tail -5' %f)
                    if status == 0 and output.strip() != "":
                        rep_context = ip_list[2] + "." + ip_list[3] + ":" + f
                        #context = output.replace('\n','\n%s:' %rep_context)
                        context = '\n' + '---------\n' + rep_context + '\n' + output
                        producer.send('Monitor_Log_Traceback', context)
                        producer.flush()
    except:
        print "Except Error in search_keys:%s" % traceback.format_exc()

if __name__ == '__main__':
    try:
        search_keys()
    except:
        print "Except Error:%s" % traceback.format_exc()
