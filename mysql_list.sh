#! /bin/bash
#set -x -e
PATH=/usr/local/bin:/bin:/usr/bin:/usr/sbin/
export PATH
salt '1.1.1.1' cmd.run 'mysql -e "show databases" |egrep -v "Database|information_schema|mysql|test"' > /data1/shell/247_full_new
salt '2.2.2.2' cmd.run 'find /data/mysql/data/ -type d -exec du -sh {} \; |egrep -v "test" |grep G |sed "1d" |awk -F "[ /]+" "{print \$1,\$NF}"' > /data1/shell/247_big
########################
salt '3.3.3.3' cmd.run 'mysql -e "show databases" |egrep -v "Database|information_schema|mysql|test|zabbix|B2B"' > /data1/shell/253_full_new
salt '3.3.3.3' cmd.run 'find /data/mysql/data/ -type d -exec du -sh {} \; |egrep -v "test|zabbix|B2B" |grep G |sed "1d" |awk -F "[ /]+" "{print \$1,\$NF}"' > /data1/shell/253_big
##########################
salt '4.4.4.4' cmd.run 'mysql -e "show databases" |egrep -v "Database|information_schema|mysql|test"' > /data1/shell/219_full_new
salt '5.5.5.5' cmd.run 'find /data/mysql/data/ -type d -exec du -sh {} \; |egrep -v "test" |grep G |sed "1d" |awk -F "[ /]+" "{print \$1,\$NF}"' > /data1/shell/219_big
############################
for i in `ls -l /data1/shell/* |awk '{print $NF}' |egrep 'new|big'`
do
	sed -i '1d' $i
	sed -i 's/^[ \t]*//g' $i
done

if [ -f /data1/shell/247_full ]
then
	diff /data1/shell/247_full_new /data1/shell/247_full > /dev/null
	if [ $? != 0 ]
	then
		\cp -raf /data1/shell/247_full_new /data1/shell/247_full
	fi
else
	\cp -raf /data1/shell/247_full_new /data1/shell/247_full
fi

if [ -f /data1/shell/253_full ]
then
        diff /data1/shell/253_full_new /data1/shell/253_full > /dev/null
        if [ $? != 0 ]
        then
                \cp -raf /data1/shell/253_full_new /data1/shell/253_full
        fi
else
	\cp -raf /data1/shell/253_full_new /data1/shell/253_full
fi

if [ -f /data1/shell/219_full ]
then
        diff /data1/shell/219_full_new /data1/shell/219_full > /dev/null
        if [ $? != 0 ]
        then
                \cp -raf /data1/shell/219_full_new /data1/shell/219_full
        fi
else
	\cp -raf /data1/shell/219_full_new /data1/shell/219_full
fi

rm -rf /data1/shell/247_small
rm -rf /data1/shell/253_small
rm -rf /data1/shell/219_small

while read line
do
   grep -iq $line /data1/shell/247_big
   if [ $? != 0 ]
   then
	echo $line >> /data1/shell/247_small
   fi
done < /data1/shell/247_full

while read line
do
   grep -iq $line /data1/shell/253_big
   if [ $? != 0 ]
   then
        echo $line >> /data1/shell/253_small
   fi
done < /data1/shell/253_full

while read line
do
   grep -iq $line /data1/shell/219_big
   if [ $? != 0 ]
   then
        echo $line >> /data1/shell/219_small
   fi
done < /data1/shell/219_full
##########################################
\cp -raf /data1/shell/*_small /srv/salt/package/mysql_list/
\cp -raf /data1/shell/*_big /srv/salt/package/mysql_list/
