#!/usr/local/bin/python
# -*- coding:utf-8 -*-
"""Stat Codis Module"""

import sys,os
import redis
import MySQLdb
import time
import traceback
import optparse
from Queue import Queue
from gevent.pool import Group
import gevent
import gevent.monkey
gevent.monkey.patch_all()
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

reload(sys)
sys.setdefaultencoding('utf-8')
MAX_STAT_LEVEL = 4
PRINT_INTERVAL = 100000
MIN_NUM_KEYS_FOR_PRINT = 1000

class CodisTools:

    def __init__(self):
        self.codis_servers = [
                                #{'ip':'1.1.1.1', 'port':6382, 'pass':''},                                            # Online Codis 
                                #{'ip':'2.2.2.2', 'port':6380, 'pass':''},                                            # Online Codis 
                                #{'ip':'3.3.3.3', 'port':6382, 'pass':''},                                            # Online Codis
                                {'ip':'4.4.4.4', 'port':6380, 'pass':''},                                            # Online Codis
                             ]

        self.redis_clients = {}
        for redis_no in range(len(self.codis_servers)):
            redis_host = self.codis_servers[redis_no]
            if redis_host['pass']:
                self.redis_clients[redis_no] = redis.Redis(redis_host['ip'], redis_host['port'], password=redis_host['pass'])
            else:
                self.redis_clients[redis_no] = redis.Redis(redis_host['ip'], redis_host['port'])
        self.keys_queue = Queue()
        self.mysql_server = ['1.1.1.1', '3306', 'user', 'aaaaa', 'db_name']
    def display(self):
        print self.redis_clients

    def list_codis_server(self):
        try:
            print u"目前有%d个codis_server节点" % len(self.codis_servers)
            for s in self.codis_servers:
                print "codis server node:%s:%s" % (s['ip'], s['port'])
            return
        except:
            print "except in list_codis_server:%s" % traceback.format_exc()
            return
	
    def send_mail(self, title, to_list, sub, filename):
	try:
	    me = title+"<"+mail_user+">"
	    msg = MIMEMultipart('related')
	    msg['Subject'] = sub
	    msg['From'] = me
	    msg['To'] = ";".join(to_list)
	    att = MIMEText(open(filename, 'rb').read(),_subtype='plain',_charset='gb2312')
	    att["Content-Type"] = 'application/octet-stream'
	    att["Content-Disposition"] = 'attachment; filename=%s' %os.path.split(filename)[1]
	    msg.attach(att)

	    server = smtplib.SMTP()  
            server.connect(mail_host)  
            server.login(mail_user,mail_pass)  
            server.sendmail(me, to_list, msg.as_string())  
            server.close()
	except:
            print "except in send_mail:%s" % traceback.format_exc()
            return
	
    def scan_keys(self, redis_no, patten, max_count):
        try:
            cursor = 0
            #total_scan_keys = 0
            while True:
                try:
                    if patten:
                        cursor, keys = self.redis_clients[redis_no].scan(cursor=cursor, match=patten, count=max_count)
                    else:
                        cursor, keys = self.redis_clients[redis_no].scan(cursor=cursor, count=max_count)
                    if cursor:
                        for k in keys:
                            self.keys_queue.put((k, redis_no))
                    else:
                        self.keys_queue.put(("redis scan over",redis_no))
                        break
                    #total_scan_keys += len(keys)
                    #if total_scan_keys % 10000 == 0:
                    #    print "host:%s, scan %d keys" % (self.codis_servers[redis_no], total_scan_keys)
                except:
                    print "scan redis except:%s" % traceback.format_exc()
                    gevent.sleep(1.0)
            #print "%s scan keys done!" % self.codis_servers[redis_no]
            return
        except:
            print "except in scan_keys%s" % traceback.format_exc()
            return


    def print_stat(self, stats):
        try:
            for prekey in stats:
                if stats[prekey]['num_keys'] < MIN_NUM_KEYS_FOR_PRINT:
                    continue
                mem_size = "%.3f" % (stats[prekey]['mem_size']*1.0 / 1024 / 1024)
                print "[PrefixKey] %-50s [NumKeys] %-10d [MemSize(MB)] %-10s [TTL] %-10d" % (prekey,stats[prekey]['num_keys'],mem_size,stats[prekey]['ttl'])
        except:
            print "except in print_stat:%s" % traceback.format_exc()
    
    def mysql_stat(self, stats):
	try:
	    mysql_conn = MySQLdb.connect(host=self.mysql_server[0], port=int(self.mysql_server[1]), user=self.mysql_server[2], passwd=self.mysql_server[3], db=self.mysql_server[4])
	    cursor = mysql_conn.cursor()
	    for prekey in stats:
                if stats[prekey]['num_keys'] < MIN_NUM_KEYS_FOR_PRINT:
		    continue
		mem_size = "%.3f" % (stats[prekey]['mem_size']*1.0 / 1024 / 1024)
		cursor.execute("insert into redis_stat_count (`keysname`,`keysnum`,`keysmem`,`keysttl`,`datetime`) values('%s','%s','%s','%s','%s')" %(prekey,stats[prekey]['num_keys'],mem_size,stats[prekey]['ttl'],TODAY))
	    cursor.close()
	    mysql_conn.commit()
	    mysql_conn.close()
	except:
            print "except in mysql_stat:%s" % traceback.format_exc()
    
    def parse_prefix(self, key):
        try:
            # 切分key，获取层级数据
            items = key.split(':')
            if len(items) <= 1:
                #print "no ':' key:%s" % key
                pass

            # 获取最大统计的层级
            max_stat_level = MAX_STAT_LEVEL if len(items) >= MAX_STAT_LEVEL else len(items)

            # 从顶级key开始统计
            prefix = ':'.join(items[0:max_stat_level])
            return prefix
        except:
            print "except in parse_prefix:%s" % traceback.format_exc()
            return None


    def parse_debug_info(self, redis_no, key):
        try:
            debug = self.redis_clients[redis_no].debug_object(key)
            if debug:
                return debug
            return None
        except:
            #print "except in parse_debug_info:%s" % traceback.format_exc()
            return None

    def parse_ttl(self, redis_no, key):
        try:
            ttl = self.redis_clients[redis_no].ttl(key)
            return ttl
        except:
                return 12

    def stat_keys(self, prefix_keys, stat_size, stat_ttl):
        try:
            #num_stat_keys = 0
            while True:
                try:
                    # 获取key
                    (k, redis_no) = self.keys_queue.get()
                    if k == "redis scan over":
                        break

                    # 解析key
                    prefix = self.parse_prefix(k)
                    if prefix == None:
                        continue

                    mem_size = 0
                    if stat_size:
                        # 获取key的调试信息
                        debug = self.parse_debug_info(redis_no, k)
                        if debug == None:
                            #print "key:%s no debug info" % k
                            continue
                        mem_size += debug['serializedlength']

                    #判断是否存在ttl,不存在ttl为0,存在ttl为1
                    ttl_value = 1
                    if stat_ttl:
                        ttl = self.parse_ttl(redis_no, k)
                        if ttl == 12:
                             #print "ttl have error"
                             continue
                        elif ttl == None:
                             ttl_value = 0
                        else:
                             ttl_value = 1

                    # 对key的前缀进行统计计数
                    if prefix in prefix_keys:
                        prefix_keys[prefix]['num_keys'] += 1
                        prefix_keys[prefix]['mem_size'] += mem_size
                    else:
                        prefix_keys[prefix] = {}
                        prefix_keys[prefix]['num_keys'] = 1
                        prefix_keys[prefix]['mem_size'] = 0
                        prefix_keys[prefix]['ttl'] = ttl_value
                                            #num_stat_keys += 1
                    # 固定间隔打印统计信息
                    #if num_stat_keys % PRINT_INTERVAL == 0:
                    #    self.print_stat(prefix_keys)
                except:
                    print "stat key except:%s" % traceback.format_exc()
                    continue
            #self.print_stat(prefix_keys)
        except:
            print "except in stat_keys:%s" % traceback.format_exc()
            return

    def new_scan_key(self, patten, count_per_scan):
            scan_workers = Group()
            for redis_no in self.redis_clients:
                g = gevent.spawn(self.scan_keys, redis_no, patten, count_per_scan)
                scan_workers.add(g)
            scan_workers.join()


    def new_stat_keys(self, stat_keys, stat_size, stat_ttl):
            max_concurrency = len(self.codis_servers)
            stat_workers = Group()
            for i in range(max_concurrency):
                stat_keys[i] = {}
                g = gevent.spawn(self.stat_keys, stat_keys[i], stat_size, stat_ttl)
                stat_workers.add(g)
            stat_workers.join()

    def stat(self, patten, count_per_scan, stat_size, stat_ttl):
        try:
            begin_time = time.time()
            stat_keys = {}
            print "start working..."
            group_obj = Group()
            g1 = gevent.spawn(self.new_scan_key, patten, count_per_scan)
            g2 = gevent.spawn(self.new_stat_keys, stat_keys, stat_size, stat_ttl)
            group_obj.add(g1)
            group_obj.add(g2)
            group_obj.join()

            # 组合各个server的数据
            stats = {}
            for i in stat_keys:
                for prefix in stat_keys[i]:
                    if prefix not in stats:
                        stats[prefix] = stat_keys[i][prefix]
                    else:
                        stats[prefix]['num_keys'] += stat_keys[i][prefix]['num_keys']
                        stats[prefix]['mem_size'] += stat_keys[i][prefix]['mem_size']
            #print "TotalCodisKeysStatResults    Patten[%s]" % patten
            self.print_stat(stats)
            self.mysql_stat(stats)
            #print stats
            end_time = time.time()
            interval_time = end_time - begin_time
            print "stat workers done! total time %s" %interval_time
            return True
        except:
            print "except in stat:%s" % traceback.format_exc()

    def slow_log(self):
       try:
	    begin_time = time.time()
	    name_dic = {}
	    mysql_conn = MySQLdb.connect(host=self.mysql_server[0], port=int(self.mysql_server[1]), user=self.mysql_server[2], passwd=self.mysql_server[3], db=self.mysql_server[4])
	    cursor = mysql_conn.cursor()
	    for redis_no in self.redis_clients:
		cli_list = self.redis_clients[redis_no].slowlog_get()
		#ip = self.codis_servers[redis_no]['ip']
		#port = self.codis_servers[redis_no]['port']
		#print "It's %s:%s slow log show:" %(ip,port)
		for i in cli_list:
			duration = i['duration'] / 1000
			start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(i['start_time']))
			if i['command'] not in name_dic:
				name_dic[i['command']] = [duration,start_time,i['id']]
				#print "指令: %s  执行时间: %sms  指令开始执行的时间: %s  唯一标示: %s" %(i['command'],duration,start_time,i['id'])
			else:
				if duration > name_dic[i['command']][0]:
					name_dic[i['command']][0] = duration
				else:
					continue
	    for k,v in name_dic.items():
		if len(k) < 200:
			try:
				cursor.execute("insert into redis_slow_record (`command`,`duration`,`start_time`,`com_id`) values('%s','%s','%s','%s')" %(k.decode('utf-8'),v[0],v[1],v[2]))
			except:
				pass
	    cursor.close()
            mysql_conn.commit()
            mysql_conn.close()
	    end_time = time.time()
	    interval_time = end_time - begin_time
	    #print interval_time
	except:
	    print "except in slow_log:%s" % traceback.format_exc()

    def parse_ttl(self):
	try:
	    mysql_conn = MySQLdb.connect(host=self.mysql_server[0], port=int(self.mysql_server[1]), user=self.mysql_server[2], passwd=self.mysql_server[3], db=self.mysql_server[4])
            cursor = mysql_conn.cursor()
	    cursor.execute("SELECT distinct keysname from redis_stat_count WHERE keysttl=0")
	    result = cursor.fetchall()
	    if os.path.exists('/data/shell/no_ttl'):
  		os.remove('/data/shell/no_ttl')
	    for sql in result:
		with open('/data/shell/no_ttl','a+') as f:
			f.write(sql[0])
			f.write('\n')
	    cursor.close()
	    mysql_conn.commit()
	    mysql_conn.close()
	    self.send_mail("codis no ttl list",mailto_list,'codis alarm','/data/shell/no_ttl')
	except:
            print "except in parse_slow:%s" % traceback.format_exc()
	
    def clear_redis_data(self, redis_no, patten, max_count):
        try:
            cursor = 0
            total_num_clear = 0
            while True:
                cursor, keys = self.redis_clients[redis_no].scan(cursor=cursor, match=patten, count=max_count)
                if cursor:
                    for key in keys:
                        #print "clear key:%s" % key
                        try:
                            self.redis_clients[redis_no].delete(key)
                            total_num_clear += 1
                        except:
                            print traceback.format_exc()
                            continue
                    #print "RedisServer[%s], Patten[%s], ClearKeys[%d]" % (self.codis_servers[redis_no], patten, total_num_clear)
                else:
                    print "RedisServer[%s], Patten[%s] Clear Done!" % (self.codis_servers[redis_no], patten)
                    break
            return
        except:
            print "except in clear_redis_data:%s" % traceback.format_exc()
            return


    def clear(self, patten, count_per_scan):
        try:
            workers = []
            print "start to clear keys..."
            for redis_no in self.redis_clients:
                workers.append(gevent.spawn(self.clear_redis_data, redis_no, patten, count_per_scan))
                #print "start %s clear keys..." % self.codis_servers[redis_no]

            for w in workers:
                w.join()
            return True
        except:
            print 'except in clear:%s' % traceback.format_exc()
            return False

def option_parser():
    try:
        parser = optparse.OptionParser("python total_codis.py -h || Example For: python total_codis.py -m 2 --patten 'qunar:data:hotelsprices:*' -c 1000 --stat_size True --stat_ttl True -count False")
        parser.add_option('-m', action='store', dest='mode', type='int',
                          default=1, help=(u'工具的执行模式，1.列出所有的server节点；2.执行统计key；\
                          3.执行清理key(清理匹配patten的所有key，由于patten的默认值为*，所以请小心使用)'))
        parser.add_option('--patten', action='store', dest='patten',
                          default='*', help=u'扫描key的通配符，例如"hqs:*"，默认为"*"')
        parser.add_option('-c', action='store', dest='count_per_scan', type='int',
                          default=500, help=u'每次scan的最大key个数，默认为500个key')
        parser.add_option('--stat_size', action='store_true', dest='stat_size',
                          default=False, help=u'统计缓存的大小，这个需要对每个key执行操作，性能较慢，谨慎使用；\
                          建议对统计的key的数量不多的时候使用')
        parser.add_option('--stat_ttl', action='store_true', dest='stat_ttl',
                          default=False, help=u'统计缓存的key是否存在ttl，这个需要对每个key执行操作，性能较慢，谨慎使用；\
                          建议对统计的key的数量不多的时候使用')
        return parser
    except:
        print("Failed to create option parser.")
        return None


if __name__=="__main__":
    # parse options
    opt_parser = option_parser()
    if len(sys.argv) == 1:
        opt_parser.print_help()
        sys.exit(1)

    (options, args) = opt_parser.parse_args(sys.argv)

    codisTools = CodisTools()
    if options.mode == 1:
        codisTools.list_codis_server()
        codisTools.display()
    elif options.mode == 2:
        codisTools.stat(options.patten, options.count_per_scan, options.stat_size, options.stat_ttl)
    elif options.mode == 3:
        codisTools.slow_log()
    elif options.mode == 4:
	codisTools.parse_ttl()
    elif options.mode == 5:
        #codisTools.clear(options.patten, options.count_per_scan)
        pass
    else:
        print "illegal mode:%s" % options.mode
