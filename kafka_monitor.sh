#! /bin/bash
#获取消费组，C语言的无法获取
#/usr/local/kafka3/bin/kafka-consumer-groups.sh --bootstrap-server 1.1.1.1:8080 --list
echo > /data/script/topic.list
group_list=(B S)

if [ -f /data/script/topic_mail ];then
    rm -rf /data/script/topic_mail
fi

for g in ${group_list[@]}
do
    source /etc/profile && /usr/local/kafka3/bin/kafka-consumer-groups.sh --new-consumer --describe --bootstrap-server 1.1.1.1:8080 --group $g |egrep -v "TOPIC" >> /data/script/topic.list
done

sed -i '/^$/d' /data/script/topic.list
#sort -n -k 5 -r /data/script/ttmp.list > /data/script/topic.list
awk '{if($5>20000) print $0}' /data/script/topic.list > /data/script/topic_mail

if [ -s /data/script/topic_mail ];then
    /usr/local/bin/sendEmail -f username -t to_mail -s smtp.exmail.qq.com -u "k000" -xu  -xp  -m "See ex" -a /data/script/topic_mail
fi
-----------------------------------------------------------------------------------------------------------------
#! /bin/bash

if [ -f /data/script/repl_mail ];then
    rm -rf /data/script/repl_mail
fi

source /etc/profile && /usr/local/kafka3/bin/kafka-topics.sh --describe --zookeeper 1.1.1.1:2181|grep "Leader" |awk '{if($(NF-2) != $NF) print $0}' > /data/script/repl_list

while read line
do
    n=`echo $line |awk '{print $NF}' |tr ',' '\n' |sort |tr '\n' ','`
    n2=`echo $line |awk '{print $(NF-2)}' |tr ',' '\n' |sort |tr '\n' ','`
    if [ ${n%?} != ${n2%?} ];then
        echo $line >> /data/script/repl_mail
    fi
done < /data/script/repl_list

if [ -s /data/script/repl_mail ];then
    /usr/local/bin/sendEmail -f -t  -s s -u "kag" -xu n -xp  -m "FYI" -a /data/script/repl_mail
fi
