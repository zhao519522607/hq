#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zookeeper,redis

ser_list = []
ops = 0
handler = zookeeper.init("1.1.1.1:2181")
data = zookeeper.get_children(handler,"/zk/codis/db_hq_001/servers")
for i in data:
   i_list = zookeeper.get_children(handler,"/zk/codis/db_hq_001/servers/%s" %i)[0]
   ser_list.append(i_list)
zookeeper.close(handler)

for s_list in ser_list:
   tmp = s_list.split(':')
   r = redis.Redis(host=tmp[0], port=int(tmp[1]))
   ops += r.info()["instantaneous_ops_per_sec"]
with open('/tmp/codis_ops','w+') as f:
     f.write(str(ops))
