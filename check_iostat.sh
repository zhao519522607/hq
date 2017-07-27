#! /bin/bash
num=`ps -ef |grep "/usr/bin/iostat" |grep -v grep |wc -l`
if [ $num -lt 1 ]
then
	echo "" > /tmp/iostat_status
	/usr/bin/iostat -xdm 25 > /tmp/iostat_status &
else
	echo "" > /tmp/iostat_status
	echo "running"
fi
-----------------------------------------------------
#! /bin/bash
disk_name=$1
case $2 in
        r.tps)
               cat /tmp/iostat_status |grep -a $disk_name |awk '{print $4}' |tail -1
                ;;
        w.tps)
                cat /tmp/iostat_status |grep -a $disk_name |awk '{print $5}' |tail -1
                ;;
        r.sec)
                cat /tmp/iostat_status |grep -a $disk_name |awk '{print $6}' |tail -1
                ;;
        w.sec)
                cat /tmp/iostat_status |grep -a $disk_name |awk '{print $7}' |tail -1
                ;;
        avgque)
                cat /tmp/iostat_status |grep -a $disk_name |awk '{print $9}' |tail -1
                ;;
        await)
                cat /tmp/iostat_status |grep -a $disk_name |awk '{print $10}' |tail -1
                ;;
	svctm)
		cat /tmp/iostat_status |grep -a $disk_name |awk '{print $(NF-1)}' |tail -1
                ;;
	util)
		cat /tmp/iostat_status |grep -a $disk_name |awk '{print $NF}' |tail -1
                ;;
esac
----------------------------------------------------------------------------------------------------------------------

#!/bin/bash
diskarray=(`cat /proc/diskstats |grep -E "\bsd[abcdefg]\b|\bxvd[abcdefg]\b|\bvd[abcdefg]\b"|grep -i "\b$1\b"|awk '{print $3}'|sort|uniq 2>/dev/null`)
length=${#diskarray[@]}
printf "{\n"
printf  '\t'"\"data\":["
for ((i=0;i<$length;i++))
do
        printf '\n\t\t{'
        printf "\"{#DISK_NAME}\":\"${diskarray[$i]}\"}"
        if [ $i -lt $[$length-1] ];then
                printf ','
        fi
done
printf  "\n\t]\n"
printf "}\n"

*/30 * * * * sh /usr/local/zabbix/etc/zabbix_agentd.conf.d/check_iostat.sh > /dev/null 2>&1
