#! /bin/bash

dir=$(dirname $0)
mail_to="zhao"
mail_cmd="/usr/local/bin/sendEmail -f develop -t $mail_to -s smtp.exmail.qq.com -o message-charset=utf-8 -xu develop -xp aaa"

if [ -f $dir/mem.csv ]
then
    rm -rf $dir/mem.csv
fi

for i in `ls $dir/*.rdb`
do
    rdb -c memory $i >> $dir/mem.csv
done

if [ -f $dir/mem ]
then
    rm -rf $dir/mem
fi

cat $dir/mem.csv |awk -F '[,":]+' '{print $3}' |sort |uniq -c |sort -rn > $dir/key_num

while read line
do
    name=$(echo $line |awk '{print $2}')
    cat $dir/mem.csv |awk -F ',' -v nn=$name '/'$name':/ {sum+=$4} END{print nn,sum/1024/1024"M"}' >> $dir/mem
done < $dir/key_num

$mail_cmd -u "HOTEL CODIS" -m "HH machine memory statistics" -a $dir/mem
