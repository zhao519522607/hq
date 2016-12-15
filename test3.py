#!/usr/bin/env python
# -*- coding=utf-8 -*-

from gevent import monkey;monkey.patch_all()
import gevent
from gevent import socket
from gevent.queue import Queue
from gevent.pool import Group
from gevent import getcurrent
from Queue import Queue

info_queue = Queue()

def info1(i):
        #print('info1 Greenlet %s,index:%d'%(id(getcurrent()),i))
    info_queue.put(i)
    gevent.sleep(1)
    info_queue.put("over")

def info2():
    while True:
        i = info_queue.get(block=False)
        print i
        if i == "over":
            break
        print('info2 Greenlet %s,index:%d'%(id(getcurrent()),i))
        gevent.sleep(1)

def main():

     group_info   = Group()
     for i in range(1,6):
        g1 = gevent.spawn(info1,i)
        g2 = gevent.spawn(info2)

     group_info.add(g1)
     group_info.add(g2)

     group_info.join()

if __name__=="__main__":
    main()
