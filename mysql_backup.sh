#! /bin/bash

cmd="/usr/bin/mysqldump -R -uaa"
time1=`date +%Y%m%d%H`

help(){
	echo "-------------------------------"
	echo "option:small big1 big2 big3"
	echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	echo "other option no support"
	echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	echo '''
		small: capacity < 1G
		big1: 1G < capacity < 10G
		big2: 10G < capacity < 100G
		big3: 100G < capacity
		mysql恢复：gunzip < $db_name-$time1.sql.gz |mysql -uroot -p $db_name'''
	echo "-------------------------------"
      }

# capacity < 1G
small() {
	while read line
	do
	    $cmd -h 10.0 $line > /data1/253/small/$line-$time1.sql
	    if [ $? != 0 ]
            then
               /usr/local/bin/sendEmail -f mail -t mail -s smtp.exmail.qq.com -u "mysqldump warning" -xu aa -xp aa -m "$line dump failed,check it please."
            fi
	done < /data1/shell/list/253_small
	find /data1/253/small/ -name "*.sql" -type f -exec gzip {} \;
	while read line
        do
            $cmd -h 10.0 $line > /data1/247/small/$line-$time1.sql
	    if [ $? != 0 ]
            then
               /usr/local/bin/sendEmail -f aa -t aa -s smtp.exmail.qq.com -u "mysqldump warning" -xu aa -xp aa -m "$line dump failed,check it please."
            fi
        done < /data1/shell/list/247_small
	find /data1/247/small/ -name "*.sql" -type f -exec gzip {} \;
	while read line
        do
            $cmd -h 10.0 $line > /data1/219/small/$line-$time1.sql
	    if [ $? != 0 ]
            then
               /usr/local/bin/sendEmail -f aa -t aa -s aa -u "mysqldump warning" -xu aa -xp aa -m "$line dump failed,check it please."
            fi
        done < /data1/shell/list/219_small
	find /data1/219/small/ -name "*.sql" -type f -exec gzip {} \;
        }

#level1: 1G < capacity < 10G
#level2: 10G < capacity < 100G
#level3: 100G < capacity
big1() {
	while read line
	do
		capacity=`echo $line |awk '{print $1}' |awk -F 'G' '{print $1}'`
		if [ $(echo "$capacity < 10"|bc) -eq 1 ]
		then
			db_name=`echo $line |awk '{print $2}'`
			#echo $db_name
			$cmd -h 10.0 $db_name > /data1/253/big1/$db_name-$time1.sql
			if [ $? != 0 ]
			then
				/usr/local/bin/sendEmail -f aa -t aa -s smtp.exmail.qq.com -u "mysqldump warning" -xu aa -xp aa -m "$db_name dump failed,check it please."
			fi
		fi
	done < /data1/shell/list/253_big
	find /data1/253/big1/ -name "*.sql" -type f -exec gzip {} \;
	while read line
        do
                capacity=`echo $line |awk '{print $1}' |awk -F 'G' '{print $1}'`
                if [ $(echo "$capacity < 10"|bc) -eq 1 ]
                then
                        db_name=`echo $line |awk '{print $2}'`
                        #echo $db_name
                        $cmd -h 10.0 $db_name > /data1/247/big1/$db_name-$time1.sql
			if [ $? != 0 ]
                        then
                                /usr/local/bin/sendEmail -f aa -t aa -s aa -u "mysqldump warning" -xu aa -xp aa -m "$db_name dump failed,check it please."
                        fi
                fi
        done < /data1/shell/list/247_big
	find /data1/247/big1/ -name "*.sql" -type f -exec gzip {} \;
	while read line
        do
                capacity=`echo $line |awk '{print $1}' |awk -F 'G' '{print $1}'`
                if [ $(echo "$capacity < 10"|bc) -eq 1 ]
                then
                        db_name=`echo $line |awk '{print $2}'`
                        #echo $db_name
                        $cmd -h 10.0$db_name > /data1/219/big1/$db_name-$time1.sql
			if [ $? != 0 ]
                        then
                                /usr/local/bin/sendEmail -f aa -t aa -s smtp.exmail.qq.com -u "mysqldump warning" -xu aa -xp aa -m "$db_name dump failed,check it please."
                        fi
                fi
        done < /data1/shell/list/219_big
	find /data1/219/big1/ -name "*.sql" -type f -exec gzip {} \;
      }

big2() {
	while read line
        do
                capacity=`echo $line |awk '{print $1}' |awk -F 'G' '{print $1}'`
                if [ $(echo "$capacity > 10"|bc) -eq 1 ] && [ $(echo "$capacity < 100"|bc) -eq 1 ]
                then
                        db_name=`echo $line |awk '{print $2}'`
                        #echo $db_name
                        $cmd -h 10.0 $db_name > /data1/253/big2/$db_name-$time1.sql
			if [ $? != 0 ]
                        then
                                /usr/local/bin/sendEmail -f aa -t aa -s smtp.exmail.qq.com -u "mysqldump warning" -xu aa -xp aa -m "$db_name dump failed,check it please."
                        fi
                fi
        done < /data1/shell/list/253_big
        find /data1/253/big2/ -name "*.sql" -type f -exec gzip {} \;
        while read line
        do
                capacity=`echo $line |awk '{print $1}' |awk -F 'G' '{print $1}'`
                if [ $(echo "$capacity > 10"|bc) -eq 1 ] && [ $(echo "$capacity < 100"|bc) -eq 1 ]
                then
                        db_name=`echo $line |awk '{print $2}'`
                        #echo $db_name
                        $cmd -h 10.0 $db_name > /data1/247/big2/$db_name-$time1.sql
			if [ $? != 0 ]
                        then
                                /usr/local/bin/sendEmail -f aa -t aa -s smtp.exmail.qq.com -u "mysqldump warning" -xu aa -xp aa -m "$db_name dump failed,check it please."
                        fi
                fi
        done < /data1/shell/list/247_big
	find /data1/247/big2/ -name "*.sql" -type f -exec gzip {} \;
        while read line
        do
                capacity=`echo $line |awk '{print $1}' |awk -F 'G' '{print $1}'`
                if [ $(echo "$capacity > 10"|bc) -eq 1 ] && [ $(echo "$capacity < 100"|bc) -eq 1 ]
                then
                        db_name=`echo $line |awk '{print $2}'`
                        #echo $db_name
                        $cmd -h 10.0 $db_name > /data1/219/big2/$db_name-$time1.sql
			if [ $? != 0 ]
                        then
                                /usr/local/bin/sendEmail -f aa -t aa -s smtp.exmail.qq.com -u "mysqldump warning" -xu aa -xp aa -m "$db_name dump failed,check it please."
                        fi
                fi
        done < /data1/shell/list/219_big
	find /data1/219/big2/ -name "*.sql" -type f -exec gzip {} \;
       }

big3() {
	 while read line
        do
                capacity=`echo $line |awk '{print $1}' |awk -F 'G' '{print $1}'`
                if [ $(echo "$capacity > 100"|bc) -eq 1 ]
                then
                        db_name=`echo $line |awk '{print $2}'`
                        #echo $db_name
                        /usr/local/bin/sendEmail -f aa -t aa -s smtp.exmail.qq.com -u "mysqldump warning" -xu aa -xp aa -m "$db_name greater than,notify all please."
                fi
        done < /data1/shell/list/253_big

        while read line
        do
                capacity=`echo $line |awk '{print $1}' |awk -F 'G' '{print $1}'`
                if [ $(echo "$capacity > 100"|bc) -eq 1 ]
                then
                        db_name=`echo $line |awk '{print $2}'`
                        #echo $db_name
                        /usr/local/bin/sendEmail -f aa -t aa -s smtp.exmail.qq.com -u "mysqldump warning" -xu aa -xp aa -m "$db_name greater than,notify all please."
                fi
        done < /data1/shell/list/247_big

        while read line
        do
                capacity=`echo $line |awk '{print $1}' |awk -F 'G' '{print $1}'`
                if [ $(echo "$capacity > 100"|bc) -eq 1 ]
                then
                        db_name=`echo $line |awk '{print $2}'`
                        #echo $db_name
                        /usr/local/bin/sendEmail -f aa -t aa -s aa -u "mysqldump warning" -xu aa -xp aa -m "$db_name greater than,notify all please."
                fi
        done < /data1/shell/list/219_big
	}

case $1 in
	small)
		small
		find /data1/219/small/ -type f -ctime +2 -exec rm -rf {} \;
		find /data1/247/small/ -type f -ctime +2 -exec rm -rf {} \;
		find /data1/253/small/ -type f -ctime +2 -exec rm -rf {} \;
		find /data1/219/small/ -type f -ctime -1 > /data1/shell/small.list
		find /data1/247/small/ -type f -ctime -1 >> /data1/shell/small.list
		find /data1/253/small/ -type f -ctime -1 >> /data1/shell/small.list
		python /data1/shell/upload_oss.py /data1/shell/small.list
		;;
	big1)
		rm -rf /data1/219/big1/*
		rm -rf /data1/247/big1/*
		rm -rf /data1/253/big1/*
		big1
		find /data1/219/big1/ -type f > /data1/shell/big1.list
                find /data1/247/big1/ -type f >> /data1/shell/big1.list
                find /data1/253/big1/ -type f >> /data1/shell/big1.list
		python /data1/shell/upload_oss.py /data1/shell/big1.list
		;;
	big2)
		rm -rf /data1/219/big2/*
                rm -rf /data1/247/big2/*
                rm -rf /data1/253/big2/*
		big2
		find /data1/219/big2/ -type f > /data1/shell/big2.list
                find /data1/247/big2/ -type f >> /data1/shell/big2.list
                find /data1/253/big2/ -type f >> /data1/shell/big2.list
                python /data1/shell/upload_oss.py /data1/shell/big2.list
		;;
	big3)
		big3
		;;
	*)
		help
		;;
esac
