#! /bin/bash
netstat -na |grep :80 > /data/shell/netstat.list-$(date +"%F-%H%M")
netstat -na |grep :80 |awk '{print $4}' |awk -F: '{if($2!=8000&&$2!=3306)print $2}' > /tmp/port.list
while read line
do
	lsof -i:$line > /data/shell/lf-$(date +"%F-%H%M")
done < /tmp/port.list
ps -ef > /data/shell/ps.list-$(date +"%F-%H%M")
