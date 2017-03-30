#! /bin/bash
disk_name=$1
case $2 in
        r.tps)
               cat /tmp/iostat_status |grep $disk_name |awk '{print $4}'
                ;;
        w.tps)
                cat /tmp/iostat_status |grep $disk_name |awk '{print $5}'
                ;;
        r.sec)
                cat /tmp/iostat_status |grep $disk_name |awk '{print $6}'
                ;;
        w.sec)
                cat /tmp/iostat_status |grep $disk_name |awk '{print $7}'
                ;;
        avgque)
                cat /tmp/iostat_status |grep $disk_name |awk '{print $9}'
                ;;
        await)
                cat /tmp/iostat_status |grep $disk_name |awk '{print $10}'
                ;;
	svctm)
		cat /tmp/iostat_status |grep $disk_name |awk '{print $11}'
                ;;
	util)
		cat /tmp/iostat_status |grep $disk_name |awk '{print $12}'
                ;;
esac
