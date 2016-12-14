#! /bin/bash

if [ -s /data1/shell/pid_temp ]
then
	while read line
	do
		pid=`echo $line |awk '{print $2}'`
		name=`echo $line |awk '{print $1}'`
		/usr/bin/supervisorctl status |grep -iq $pid
		if [ $? != 0 ]
		then
			echo "`date +"%F %H:%M"` $name 重启了" >> /data1/shell/ck_pro.log
			/usr/local/codis/codis-config -c /data/codis_proxy_9/config.ini proxy online $name
		fi
	done < /data1/shell/pid_temp
	/usr/bin/supervisorctl status |grep proxy |awk '{print $1,$4}' |awk -F ',' '{print $1}' > /data1/shell/pid_temp
else
	/usr/bin/supervisorctl status |grep proxy |awk '{print $1,$4}' |awk -F ',' '{print $1}' > /data1/shell/pid_temp
	exit 10
fi
