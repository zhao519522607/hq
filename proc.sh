#! /bin/bash
port=$1
spid=`ps -ef|grep $port|grep codis-server|awk '{print $2}'`
ppid=`ps -ef|grep $port|grep codis-proxy|awk '{print $2}'`
#echo $ppid

case $2 in

	mem)
		cat /proc/$spid/status|grep -e VmRSS |awk '{print $2}'
		;;
	cpu)
		echo `top -bn 1 -p $ppid|tail -2|head -1|awk '{ssd=NF-3} {print $ssd}'`
		;;
	*)
		echo "NO No NO."
		;;
esac
