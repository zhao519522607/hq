#!/bin/bash

DB_tool=$(which mysql)
Mysql_cmd="$DB_tool -hmysql-host -uuser -ppass db -se"
Threshold=6000
CurrentHour=`date +%H`
CurrentYear=`date +%Y`
LogFileOutPut="/tmp/LastHourIPRequestGt6000.log"
Recipient="list"
MailSubject="`hostname`(`hostname -i`): 上一小时请求次数超过${Threshold}的列表"

if [ $CurrentHour -eq 00 ];then
    FilterString="\/$CurrentYear:23:"
    YesterdayLogFile="/mnt/logs/bc_logs_split/bc.access_`date +%F -d -1day`.log.gz"
    zgrep "$FilterString" $YesterdayLogFile|awk -F "\"" '{if($(NF-1)!="-"){print $(NF-1)}}'|awk -F "," '{print $1}'|sort|uniq -c|sort -k1nr|awk '{if($1>'$Threshold'){print $0}}' > $LogFileOutPut
else
    LastHour=`date +%H -d -1hour`
    FilterString="\/$CurrentYear:$LastHour:"
    LogFileInPut="/mnt/logs/access_logs/www_com.access.log"
    awk -F "\"" '/'$FilterString'/ {if($(NF-1)!="-"){print $(NF-1)}}' $LogFileInPut|awk -F "," '{print $1}'|sort|uniq -c|sort -k1nr|awk '{if($1>'$Threshold'){print $0}}' > $LogFileOutPut
fi

if [ -s $LogFileOutPut ];then
     while read line
    do
      ip=$(echo $line |awk '{print $2}')
	    sql_num=$($Mysql_cmd "SELECT * from hotelprice_ip WHERE IP='$ip';" |wc -l)
    	if [ $sql_num -eq 0 ];then
	    cra_num=$($Mysql_cmd "SELECT * crawler_ip WHERE IP='$ip';" |wc -l)
	    if [ $cra_num -eq 0 ];then
                $Mysql_cmd "INSERT INTO crawler_ip (IP) VALUES('$ip');"
	    else
		$Mysql_cmd "UPDATE crawler_ip SET NUM=NUM+1 WHERE IP='$ip';"
	    fi
	fi
    done < $LogFileOutPut
    mail -s "$MailSubject" $Recipient < $LogFileOutPut &>/dev/null
    rm -f $LogFileOutPut
fi
