#!/bin/sh

# Change the following variables for different services
EXENAME=name

# The followings are common code for Poco server applications
WORKDIR=$(cd `dirname $0`; pwd)"/../bin/"
PIDFILE=$WORKDIR/$EXENAME.pid
LAUNCH_CMD="./$EXENAME --daemon --pidfile=$PIDFILE"
M_DIR=`pwd`
M_CONF=$M_DIR/../bin/name.properties
M_DATA=$M_DIR/../data/

cd $WORKDIR
usage()
{
    echo "usage : `basename $0` start|stop|restart|status"
}

check_pb() 
{
     config_index=`grep "inv_index_file" $M_CONF |awk -F '=' '{print $2}' |awk -F ',' '{print NF}'`
     data_index=`ls -l $M_DATA |grep "index.pb*" |wc -l`
     if [ $config_index != $data_index ];then
        s_list=`ls -l $M_DATA |grep "index.pb*" |awk '{print $NF}' |tr '\n' ','`
        sed -i "s/inv_index_file=.*/inv_index_file=${s_list%?}/g" $M_CONF
     fi
     config_content=`grep "content_file" $M_CONF |awk -F '=' '{print $2}' |awk -F ',' '{print NF}'`
     data_content=`ls -l $M_DATA |grep "search_content.pb*" |wc -l`
     if [ $config_content != $data_content ];then
        s1_list=`ls -l $M_DATA |grep "search_content.pb*" |awk '{print $NF}' |tr '\n' ','`
        sed -i "s/content_file=.*/content_file=${s1_list%?}/g" $M_CONF
     fi
}

start()
{
    echo -e "Starting $EXENAME:                           `date`"
    check_pb
    if [ -f "$PIDFILE" ]; then
        server_pid=`cat $PIDFILE`
        stat=`pgrep $EXENAME | grep " $server_pid " | wc -l`
    else
        stat=0
    fi
    if [ $stat -lt 1 ] ; then
        $LAUNCH_CMD

        if [ $? -ne 0 ] ; then
            echo -e "[\033[31;1mFailed\033[m] `date`"
        else
            echo -e "[\033[34;1mOK\033[m] `date`"
        fi
    else 
        echo -e "[\033[31;1mFailed\033[m] some $EXENAME process is running ... `date`"
    fi
}

stop()
{
    echo -e "Stopping $EXENAME:                           `date`"

    if [ -f "$PIDFILE" ]; then
        server_pid=`cat $PIDFILE`
        kill -9 $server_pid 2> /dev/null
        sleep 1
        if [ $? -ne 0 ] ; then
            echo -e "[\033[31;1mFailed\033[m] $EXENAME service is not running. `date`"
        else 
            echo -e "[\033[34;1mOK\033[m] `date`"
        fi
    else
        echo -e "[\033[34;1mOK\033[m] `date`"
    fi
}

restart()
{
    stop
    echo -e "Restarting $EXENAME:                           `date`"
    check_pb
    trycount=1
    while [ "$trycount" -lt 60 ]; do
        if [ -f "$PIDFILE" ]; then
            server_pid=`cat $PIDFILE`
            stat=`pgrep $EXENAME | grep " $server_pid " | wc -l`
        else
            stat=0
        fi
        if [ $stat -lt 1 ] ; then
            echo -e "Starting $EXENAME service ..."
            $LAUNCH_CMD
            if [ $? -ne 0 ] ; then
                echo -e "[\033[31;1mFailed\033[m] `date`"
            else
                echo -e "[\033[34;1mOK\033[m] `date`"
            fi    
            break
        else 
            echo -e "$EXENAME is still running .."
        fi
        trycount=$(($trycount+1))
        sleep 5
    done
}

status()
{
    if [ -f "$PIDFILE" ]; then
        server_pid=`cat $PIDFILE`
        stat=`pgrep $EXENAME | grep " $server_pid " | wc -l`
    else
        stat=0
    fi
    if [ $stat -lt 1 ] ; then
        echo -e "$EXENAME service is stopped."
    else
        echo -e "$EXENAME service is running ..."
    fi
}

if [ $# -lt 1 ] ; then
    usage
    exit 1
fi

case "$1" in
"start")
    start
    ;;
"stop")
    stop
    ;;
"restart")
    restart
    ;;
"status")
    status
    ;;
*)
    usage
    ;;
esac
