CREATE TABLE `redis_stat_count` (
 `id` INT(11) not null AUTO_INCREMENT COMMENT '自增id',
 `keysname` varchar(100) DEFAULT NULL COMMENT 'key的名字',
 `keysnum` int(20) DEFAULT NULL COMMENT '扫描的key的数量',
 `keysmem` float(20) DEFAULT NULL COMMENT '扫描的key的内存大小，单位MB',
 `keysttl` int(2) DEFAULT NULL COMMENT 'key是否设置了ttl,0表示没有,1表示设置了',
 `datetime` date DEFAULT NULL COMMENT '插入数据的时间',
 PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='codis的key的数量、内存、ttl的状态统计'
