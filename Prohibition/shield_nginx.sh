#！/bin/bash
# Author by: zyb
# Date time: 2019-3-11

Work_dir=$(dirname $0)
DB_tool=$(which mysql)
Mysql_cmd="$DB_tool -hmysql-host -uuser -ppass db -se"
deny_file="/usr/local/nginx/conf/denyip.conf"
Mail_to="list"
Mail_cmd="/usr/local/bin/sendEmail -f user -t $Mail_to -s smtp.exmail.qq.com -o message-charset=utf-8 -xu aa.com -xp nn"

rm -rf $Work_dir/deny_record
rm -rf $Work_dir/release_record
ip_list=$($Mysql_cmd "SELECT ip from excess_ip;")

for ip in $ip_list
do
        egrep -iq "$ip" $deny_file
        if [ $? -ne 0 ];then
                echo "$ip no;" >> $deny_file
                echo "$ip 触犯规则已被封禁" >> $Work_dir/deny_record
                $Mysql_cmd "DELETE FROM excess_ip where IP='$ip';"
                deny_num=$($Mysql_cmd "SELECT * from release_ip WHERE IP='$ip';" |wc -l)
                if [ $deny_num -eq 0 ];then
                        $Mysql_cmd "INSERT INTO release_ip (IP) VALUES('$ip');"
                fi
	else
		$Mysql_cmd "DELETE FROM excess_ip where IP='$ip';"
        fi
done

if [ -s $Work_dir/deny_record ];then
       rsync -avzP /usr/local/nginx/conf/denyip.conf 172.16.20.95:/mnt/shell/
       $Mail_cmd -u "nginx封禁ip提醒" -o message-file=$Work_dir/deny_record
fi

#release_ip=$($Mysql_cmd "select ip from release_ip where MTIME <= now()-interval 2 MINUTE;")
release_ip=$($Mysql_cmd "select ip from release_ip where MTIME <= now()-interval 1 HOUR;")
permanent_ip=$($Mysql_cmd "select ip from permanent_ip where MTIME <= now()-interval 1 HOUR;")
if [ -n "$release_ip" -a -z "$permanent_ip" ];then
        for ip in $release_ip
        do
                sed -i "/$ip/"d $deny_file
                echo "$ip 封禁已满足一个小时已解禁" >> $Work_dir/release_record
                $Mysql_cmd "DELETE FROM release_ip where IP='$ip';"
		p_num=$($Mysql_cmd "select * from permanent_ip where IP='$ip';" |wc -l)
		if [ $p_num -eq 0 ];then
                	$Mysql_cmd "INSERT INTO permanent_ip (IP) VALUES('$ip');"
		fi
        done
else
	re_num=$($Mysql_cmd "select * from release_ip where IP='$ip';" |wc -l)
	if [ $re_num -gt 0 ];then
		$Mysql_cmd "DELETE FROM release_ip where IP='$ip';"
	fi
fi

if [ -s $Work_dir/release_record ];then
       rsync -avzP /usr/local/nginx/conf/denyip.conf 172.16.20.95:/mnt/shell/
       $Mail_cmd -u "nginx解禁ip提醒" -o message-file=$Work_dir/release_record
fi

if [ -s $Work_dir/deny_record -o -s $Work_dir/release_record ];then
	/usr/local/nginx/sbin/nginx -s reload
fi
