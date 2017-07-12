#!/usr/local/bin/python2.7
# -*- coding=utf-8 -*-

import sys
import time
import math
import random
import json
import httplib
#import db_connector
from utils import *
import optparse
import threading
import signal
import pdb
import traceback

CHECK_SEARCHSTABLE_URLS = {
    'hotel_demo': '/s?t=tips&q=曼谷拉查丹利中心酒店',
    'city_demo' : '/s?t=tips&q=新加坡' ,
    'ear_demo'  : '/s?t=tips&q=xidan',
}

def check_stabel_url(host, url,stable_name):
    try:
        http_conn = httplib.HTTPConnection(host, timeout=REQUEST_TIMEOUT)

        # request the url
        try:
            http_conn.request('GET', url, headers=HTTP_HEADER)
        except:
            cprint_error('FAIL URL: %s [RequestError]' % url)
            return False

        try:
            response = http_conn.getresponse()
            if not response:
                cprint_error('FAIL URL: %s [NoResponse]' % url)
                return False
            if response.status != 200:
                cprint_error('FAIL URL: %s [StatusCode:%d]' % (url, response.status))
                return False
        except:
            cprint_error('Exception in checking response status of URL: %s' % url)
            return False

        if host in HAOQIAO_HOSTS:
            return True

        # check the response content further for json results
        try:
            res = response.read()
            if not res:
                cprint_error('FAIL URL: %s [ReadResponseError]' % url)
                return False
            try:
                res_dec = res.decode('utf-8')
            except:
                cprint_error('FAIL URL: %s [DecodeResponseError]' % url)
                return False
            try:
                json_res = json.loads(res_dec)
                if not json_res or json_res['status'] == 'ERROR':
                    cprint_error('FAIL URL: %s [JsonResultError]' % url)
                    return False
            except:
                cprint_error('FAIL URL: %s [JsonLoadError]' % url)
                return False
            try:
                if stable_name == 'hotel_demo':
                    for j in json_res['hits']:
                        if 'hotel' in j:
                            if j['hotel'][0]['cn_name'] == '曼谷'.decode('utf-8') and j['hotel'][0]['country'] == '泰国'.decode('utf-8') and j['hotel'][0]['en_name'] == 'Grande Centre Point Hotel Ratchadamri'.decode('utf-8'):
                                return True
                elif stable_name == 'city_demo' and json_res['hits'][0]['city'][0]['cn_name'] == '新加坡'.decode('utf-8') and json_res['hits'][0]['city'][0]['country'] == '新加坡'.decode('utf-8') and json_res['hits'][0]['city'][0]['en_name'] == 'Singapore'.decode('utf-8'):
                    return True
                elif stable_name == 'ear_demo':
                    for j in json_res['hits']:
                        if 'attraction' in j:
                            if j['attraction'][0]['cn_name'] == '西单'.decode('utf-8') and j['attraction'][0]['country'] == '中国大陆'.decode('utf-8') and j['en_name'] == 'Xidan'.decode('utf-8'):
                                return True
                else:
                    return False
            except:
                cprint_error('FAIL URL: %s [Contrast failure]' % url)
                return False
        except:
            cprint_error('Exception in reading response content of URL: %s' % url)
            return False

        return True
    except:
        tprint_error('Exception in checking url: %s' % url)
        tprint_error(traceback.format_exc())
        return False
    finally:
        http_conn.close()
       
def do_check_stable(host_type, server_host):
    try:
        if host_type not in SERVERS:
            tprint_error('Invalid host_type given: %s' % host_type)
            return False
        if not server_host:
            tprint_error('Invalid server_host given: %s' % server_host)
            return False
        for stable_name in CHECK_SEARCHSTABLE_URLS:
            url = CHECK_SEARCHSTABLE_URLS[stable_name] + LOCAL_TEST_FLAG
            if not check_stabel_url(server_host, url, stable_name):
                return False
        return True
    except:
        tprint_error("Exception in do_check_stable")
        return False
