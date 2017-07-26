#!/usr/local/bin/python
# -*- coding:utf-8 -*-
import redis
import traceback
import MySQLdb
import socket
import requests
import random

def ali_redis():
    try:
        r = redis.Redis(host='',port=6379,password='')
        r.set('recovery:test003','aliredis')
        if r.get('recovery:test003') == 'aliredis':
            print "aliyun redis write-read is ok!"
            r.delete('recovery:test003')
    except:
        print "except in ali_redis:%s" % traceback.format_exc()

def mysql(host,user,password,db_name):
    try:
        conn = MySQLdb.connect(host=host, port=3306, user=user, passwd=password,db=db_name)
        cur = conn.cursor()
        cur.execute("create table recovery_test_name001(id int,name varchar(20),class varchar(30),age varchar(10))")
        cur.execute("insert into recovery_test_name001 values('2','Tom','3 year 2 class','9')")
        cur.execute("drop table recovery_test_name001")
        cur.close()
        conn.commit()
        conn.close()
        print "%s databases is ok!" %host
    except:
        print "%s except in mysql:%s" % (host,traceback.format_exc())

def slb(host,port):
    try:
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(2)
        sk.connect((host,port))
        print "slb %s is ok!" %host
        sk.close()
    except:
        print "%s except in slb:%s" % (host,traceback.format_exc())
