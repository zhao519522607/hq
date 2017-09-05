. ../shell/load
PROJECT=" "                           #这个要个参数要和jenkins的项目名字还有update脚本里的PROJECT一致
USER=www
IP="内网ip"
DIR="/mnt/upload/"
CONF_NAME=" "
#加载公共模块
Load ssh
Load zip
#处理配置文件
for c_name in $CONF_NAME
do
	python ../shell/oper_oss.py -m download -f $c_name
done
\cp -r /data1/jenkins_dir/conf/www_service/* application/config/
#功能函数操作
gzip $PROJECT
rm -rf applicati/aa
for i in $IP
do
	upfile $PROJECT $USER $i $DIR
done

rm -rf ../package/$PROJECT.tgz

for i in $IP
do
	cmd $USER $i "sh /mnt/upload/aaa.sh ${action} ${roll_ver}"
done
