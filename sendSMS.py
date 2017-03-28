#!/usr/bin/python
# -*- coding=utf-8 -*-

import sys
import time
import requests
import json

log_file = '/tmp/SMS.log'
URL = "http://aaa.com/send"

def out_put(msg):
    with open(log_file, 'a') as f:
        f.write(msg)
        f.write('\n')

def send_sms(phonum,subject,msg,retry=True):
    try:
        param_value = json.dumps({"info":msg})
        value = {"sender":"Zabbix-Server", "mobile":phonum, "templateid":"1", "param":param_value}
        resp = requests.post(URL, data=value)
        resp.status = resp.status_code
        response_data = resp.text

        if resp.status != 200:
            if retry:
                out_put("Failed to request text=%s, status=%d, [%s]" %\
                                  (value, resp.status, response_data))
                time.sleep(1)
                return send_sms(phonum, subject, msg, False)
            else:
                out_put("Failed to request text=%s, status=%d, [%s]" %\
                                  (value, resp.status, response_data))
        else:
            out_put("success to request text=%s, status=%d, [%s]" %\
                                  (value, resp.status, response_data))
        return True
    except Exception as e:
        print 'Exception in sms:', str(e)
        return False

#-------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 3:
        out_put('argv not enough : ' + sys.argv)
    if send_sms(sys.argv[1], sys.argv[2], sys.argv[3]):
        out_put('send sms OK %s' % (sys.argv[1]))
    else:
        out_put('send sms FAIL %s' % (sys.argv[1]))
