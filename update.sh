#! /bin/bash

update() {
	#保留最近3次的更新目录
	ls -lt /data1/web/ |tail -n +2 |awk 'BEGIN {FS=" "} NR > 3 {print $NF}' |xargs -i rm -rf /data1/web/{}
	#解压
	tar zxf /data1/upload/hqs_test.tgz -C /data1/web/
	name=hqs_test-$(date +"%F-%H%M")
	mv /data1/web/hqs_test /data1/web/$name
	if [ -h "/www/hqs_test" ];then
		rm -rf /www/hqs_test
		ln -s /data1/web/$name /www/hqs_test
	fi
}

rollback() {
	dir_ver=`ls -lt /data1/web/ |tail -n +2 |awk -v arg=$roll_v 'BEGIN {FS=" "} NR==arg {print $NF}'`
	if [ -h "/www/hqs_test" ];then
		rm -rf /www/hqs_test
		ln -s /data1/web/$dir_ver /www/hqs_test
	fi

}

case $1 in
	update)
		update
		;;
	rollback)
		roll_v=$2
		rollback
		;;
esac
