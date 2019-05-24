#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zookeeper,redis
import time

zookeeper.set_debug_level(zookeeper.LOG_LEVEL_ERROR)
ser_list = []
ops = 0

def codis_ops():
        handler = zookeeper.init("1.1.1.1:2181")
        data = zookeeper.get_children(handler,"/zk/codis/db/servers")
        for i in data:
                i_list = zookeeper.get_children(handler,"/zk/codis/db/servers/%s" %i)[0]
                ser_list.append(i_list)
        zookeeper.close(handler)

if __name__ == '__main__':
        try:
                codis_ops()
        except:
                time.sleep(2)
                codis_ops()

        for s_list in ser_list:
                tmp = s_list.split(':')
                r = redis.Redis(host=tmp[0], port=int(tmp[1]))
                ops += r.info()["instantaneous_ops_per_sec"]
        with open('/tmp/codis_ops','w+') as f:
                f.write(str(ops))
