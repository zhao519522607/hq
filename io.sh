#! /bin/bash
disk_name=$1
case $2 in
	read.ops)
	       cat /proc/diskstats |grep $disk_name |head -1 | awk '{print $4}'
		;;
	read.ms)
		cat /proc/diskstats |grep $disk_name |head -1 | awk '{print $7}'
		;;
	write.ops)
		cat /proc/diskstats |grep $disk_name |head -1 | awk '{print $8}'
		;;
	write.ms)
		cat /proc/diskstats |grep $disk_name |head -1 | awk '{print $11}'
		;;
	read.sectors)
		cat /proc/diskstats |grep $disk_name |head -1 | awk '{print $6}'
		;;
	write.sectors)
		cat /proc/diskstats |grep $disk_name |head -1 | awk '{print $10}'
		;;
esac
