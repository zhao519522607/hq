#! /bin/bash

dirname=`pwd`
name_list=`ls -l $dirname |sed '1d' |awk '{print $NF}' |grep "^[0-9]"`

rm -rf $dirname/mail

for i in $name_list
do
    grep "^Biggest" $dirname/$i |awk '{if($(NF-1)>1000000)print $4,$(NF-1)}' >> $dirname/mail
done

/usr/local/bin/sendEmail -f 111 -t 111 -s smtp.exmail.qq.com -u "codis bigkeys warning" -xu 111 -xp 11 -m "FYI" -a $dirname/mail
