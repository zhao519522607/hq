CREATE TABLE `redis_stat_count` (
 `id` INT(11) not null AUTO_INCREMENT COMMENT '自增id',
 `keysname` varchar(100) DEFAULT NULL COMMENT 'key的名字',
 `keysnum` int(20) DEFAULT NULL COMMENT '扫描的key的数量',
 `keysmem` float(20) DEFAULT NULL COMMENT '扫描的key的内存大小，单位MB',
 `keysttl` int(2) DEFAULT NULL COMMENT 'key是否设置了ttl,0表示没有,1表示设置了',
 `datetime` date DEFAULT NULL COMMENT '插入数据的时间',
 PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='codis的key的数量、内存、ttl的状态统计'
---------------------------------------------------------------------------------------
CREATE TABLE `redis_slow_record` (
 `id` int(11) not null AUTO_INCREMENT COMMENT '自增id',
 `command` varchar(200) DEFAULT NULL COMMENT '指令详情',
 `duration` int(10) DEFAULT NULL COMMENT '指令执行时间',
 `start_time` datetime DEFAULT NULL COMMENT '指令开始时间',
 `com_id` int(10) DEFAULT NULL COMMENT '指令唯一标示',
 PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='codis慢查询语句收集'
---------------------------------------------------------------------------------------
SELECT keysname,keysnum,keysmem,datetime from redis_stat_count where keysname='$line' order by datetime desc;
SELECT command from redis_slow_record where DATE_SUB(CURDATE(), INTERVAL 10 DAY) <= date(start_time);
cat /data/shell/slow_log |awk -F ':' '{print $1":"$2":"$3":"$4}' |sort |uniq -c |awk '{if($1>10) print $0}' |grep -v 'DEBUG OBJECT'
---------------------------------------------------------------------------------------------------------------------------
