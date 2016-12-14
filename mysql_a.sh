#! /bin/bash
#while read line
#do
#    mysql -e "use $line;show tables;" > lst/$line.list
#done < list

#for i in `ls -l lst/ |grep ".list" |awk '{print $NF}'`
#do
#  d_name=`echo $i|awk -F. '{print $1}'`
#  while read line
#  do
#      mysql -e "select TABLE_NAME,UPDATE_TIME from information_schema.TABLES where TABLE_SCHEMA='$d_name' and information_schema.TABLES.TABLE_NAME='$line'" >> time/$d_name.dt
#  done < lst/$i
#done

for i in `ls -l lst/ |grep ".list" |awk '{print $NF}'`
do
  d_name=`echo $i|awk -F. '{print $1}'`
  while read line
  do
      
      num=`grep "$line" /data/mysql/bin-log/2016-12-07.log |wc -l`
      echo "$line $num" >> count/$d_name.count
  done < lst/$i
done
