#！/bin/bash
# Author by: zyb
# Date time: 2019-3-8

Work_dir=$(dirname $0)
Log_dir="/mnt/data/logs/logs_hotelprice"
Log_name=log-tj-$(date +%F).php
exce_list=("1.1.1.1" "1.2.3.4")
DB_tool=$(which mysql)
Mysql_cmd="$DB_tool -h -ucodis -p db -se"
Mail_to="list"
Mail_cmd="/usr/local/bin/sendEmail -f aa -t $Mail_to -s smtp.exmail.qq.com -o message-charset=utf-8 -xu mm -xp cc"

rm -rf $Work_dir/Record
grep 'hqs返回数据处理前|第1次请求' $Log_dir/$Log_name |awk '{a[$(NF-2)]++} END{for(i in a) print a[i],i}' > $Work_dir/all_ip_list

while read line
do
	inum=$(echo $line |awk '{print $1}')
	ip=$(echo $line |awk '{print $2}')
	sql_num=$($Mysql_cmd "SELECT * from hotelprice_ip WHERE IP='$ip';" |wc -l)
	if [ $sql_num -eq 0 ];then
		$Mysql_cmd "INSERT INTO hotelprice_ip (IP,NUM) VALUES('$ip',$inum);"
	else
		#MY_NUM=$($Mysql_cmd "SELECT NUM from hotelprice_ip WHERE IP='$ip'")
		$Mysql_cmd "UPDATE hotelprice_ip SET NUM=$inum WHERE IP='$ip'"
		#if [ -n "$MY_NUM" ];then
		#	dif_value=$[$inum-$MY_NUM]
		#	if [ $dif_value -gt 50 ];then
		#		excess_num=$($Mysql_cmd "SELECT * from excess_ip WHERE IP='$ip';" |wc -l)
		#		if [ $excess_num -eq 0 ];then
		#			for i in ${exce_list[@]}
		#			do
		#				if [ $i != $ip ];then
		#					$Mysql_cmd "INSERT INTO excess_ip (IP,NUM) VALUES('$ip',$dif_value);"
		#				fi
		#			done
		#		fi
		#		echo "$ip 5分钟请求查价次数为$dif_value" >> $Work_dir/Record
		#		#echo "$(date +"%F %H:%M:%S") $ip 5分钟请求查价次数为$dif_value" >> $Work_dir/Record
		#	fi
		#fi
	fi
done < $Work_dir/all_ip_list

#if [ -s $Work_dir/Record ];then
#	$Mail_cmd -u "请求查价次数预警" -o message-file=$Work_dir/Record
#fi
