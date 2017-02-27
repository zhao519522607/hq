#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zookeeper,os
import commands

cur_path = os.path.dirname(os.path.abspath(__file__))
cmd = "%s/redis-cli -h %s -p %s --bigkeys"

ser_list = []
handler = zookeeper.init("1.1.1.1:2181")
data = zookeeper.get_children(handler,"/zk/codis/db_001/servers")
for i in data:
   i_list = zookeeper.get_children(handler,"/zk/codis/db_001/servers/%s" %i)[0]
   ser_list.append(i_list)
zookeeper.close(handler)

for s_list in ser_list:
   tmp = s_list.split(':')
   f_name = tmp[0] + "_" + tmp[1]
   (status, output) = commands.getstatusoutput(cmd %(cur_path,tmp[0],tmp[1]))
   if status == 0:
   	with open(os.path.join(cur_path,f_name),'w+') as f:
   		f.write(output)
