#! /bin/bash
PROJECT="与jenkins保持一致"
LN_name=" "

update() {
        #保留最近3次的更新目录
        ls -lt /mnt/web/$PROJECT |tail -n +2 |awk 'BEGIN {FS=" "} NR > 3 {print $NF}' |xargs -i rm -rf /mnt/web/$PROJECT/{}
        #解压
        tar zxf /mnt/upload/$PROJECT.tgz -C /mnt/web/$PROJECT/
        name=$PROJECT-$(date +"%F-%H%M")
        find /mnt/web/$PROJECT/$PROJECT -type d -name ".svn" -exec rm -rf {} \; > /dev/null 2>&1
        mv /mnt/web/$PROJECT/$PROJECT /mnt/web/$PROJECT/$name
        if [ -h "/mnt/www/$LN_name" ];then
                rm -rf /mnt/www/$LN_name
                ln -s /mnt/web/$PROJECT/$name /mnt/www/$LN_name
		ln -s /mnt/www/voucher /mnt/web/$PROJECT/$name/voucher
        else
                ln -s /mnt/web/$PROJECT/$name /mnt/www/$LN_name
		ln -s /mnt/www/voucher /mnt/web/$PROJECT/$name/voucher
        fi
	sudo /usr/bin/kill -USR2 $(cat /var/run/php-fpm/php-fpm.pid)
}

rollback() {
        dir_ver=`ls -lt /mnt/web/$PROJECT |tail -n +2 |awk -v arg=$roll_v 'BEGIN {FS=" "} NR==arg {print $NF}'`
        if [ -h "/mnt/www/$LN_name" ];then
                rm -rf /mnt/www/$LN_name
                ln -s /mnt/web/$PROJECT/$dir_ver /mnt/www/$LN_name
        else
                ln -s /mnt/web/$PROJECT/$dir_ver /mnt/www/$LN_name
        fi
	sudo /usr/bin/kill -USR2 $(cat /var/run/php-fpm/php-fpm.pid)
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
