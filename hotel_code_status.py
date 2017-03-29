#! /usr/bin/env python
#coding=utf-8

import requests
import random
import traceback

Ip_List = {
        "1": "http://1:8000",
        "2": "http://2:8000",
        "3": "http://3:8000",
        "4": "http://4:8000"
}

URL = [
        '/hotel?type=h1',
        '/hotel?type=hot',
        '/hotel?type=hot',
        '/hotel?type=numho',
        '/hotel?type=ho'
]

ur_l = []

def Check_URL(url):
        rep = requests.get(url)
        return rep.status_code

def url_list():
        for num in Ip_List:
                u_tmp = Ip_List[num] + URL[random.randint(0,len(URL)-1)]
                ur_l.append(u_tmp)

def main():
        ck_sum = 0
        url_list()
        for l in ur_l:
                if Check_URL(l) == 200:
                        ck_sum += 1
        print ck_sum

if __name__=="__main__":
        try:
                main()
        except:
                print "except in main:%s" % traceback.format_exc()
