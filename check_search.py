#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests

url = 'http://10.1.1.1:80/s?13'

def check():
    r = requests.get(url,timeout=2)
    if r.status_code == 200 and r.json()['hits'][0]['city'][0]['cn_name'] == '新加坡'.decode('utf-8') and r.json()['hits'][0]['city'][0]['country'] == '新加坡'.decode('utf-8') and r.json()['hits'][0]['city'][0]['en_name'] == 'Singapore'.decode('utf-8'):
        return True
    else:
        return False

if __name__=="__main__":
    try:
        if check():
           print 1
        else:
           print 0
    except:
        print 0
