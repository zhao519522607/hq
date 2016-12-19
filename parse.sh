#! /bin/bash
python /data/shell/keys.py -m 2 > /data/shell/parse_1
grep "PrefixKey" /data/shell/parse_1 |awk -F '[ :]+' '{print $2}' |sort |uniq |egrep -v "[availability|haoqiao]" > /tmp/codis_sub
if [ -f /data/shell/sub_mail ];then
	rm -rf /data/shell/sub_mail
fi
while read line 
do
	grep -irq $line /data/shell/redis_sub
	if [ $? != 0 ];then
		echo $line >> /data/shell/sub_mail
	fi
done < /tmp/codis_sub
if [ -s /data/shell/sub_mail ];then
	/usr/local/bin/sendEmail -f aa -t aa -s smtp.exmail.qq.com -u "codis sub abnormal" -xu aa -xp aa -m "FYI" -a /data/shell/sub_mail
fi
