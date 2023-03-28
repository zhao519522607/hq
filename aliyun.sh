#! /bin/bash

DIR=$(cd "$(dirname "$0")";pwd)
TIME=$(date +"%F %T")

if [[ "$AMX_STATUS" != "firing" ]]; then
  exit 0
fi

#echo $AMX_ANNOTATION_value >> $DIR/log_record

if [ -n "$AMX_LABEL_node" ]; then
    echo "Start..." >> $DIR/log_record
    echo $TIME >> $DIR/log_record
    echo $AMX_LABEL_node >> $DIR/log_record
    NUM=$(grep -o "$AMX_LABEL_node" $DIR/log_record |wc -l)
fi

if [ $AMX_ALERT_LEN -gt 1 ]; then
    for i in $(seq 1 "$AMX_ALERT_LEN"); do
        ref="AMX_ALERT_${i}_LABEL_node"
        node="$(echo "${!ref}" | cut -d: -f1)"
        echo "Start..." >> $DIR/${node}_record
        echo $TIME >> $DIR/${node}_record
        echo $node >> $DIR//${node}_record
        suffix=$(echo $node |awk -F'.' '{print $(NF-1)"_"$NF}')
        expr NUM_${suffix}=$(grep -o $node $DIR/${node}_record |wc -l)
    done
fi

main() {
    if [ -n "$AMX_LABEL_node" ]; then
        if [ $NUM -ge 5 ]; then
    	    /usr/bin/python3 /data/python/oper_instance.py $AMX_LABEL_node
            if [ $? -eq 0 ];then
                echo "新记录开始..." > $DIR/log_record
                echo -e "$TIME: $AMX_LABEL_node -> 重启成功\n" >> $DIR/restart_record
            else
                echo -e "重启实例失败\n" >> $DIR/log_record
                exit 1
            fi
        else
            echo -e "关键字出现次数为$NUM,本次不进行重启!\n" >> $DIR/log_record
        fi
    fi

    if [ $AMX_ALERT_LEN -gt 1 ]; then
        for i in $(seq 1 "$AMX_ALERT_LEN"); do
    	    ref="AMX_ALERT_${i}_LABEL_node"
            node="$(echo "${!ref}" | cut -d: -f1)"
           numname=$(eval echo '$'NUM_${suffix})
            NUM=$(echo $numname |awk -F'=' '{print $2}')
            if [ $NUM -ge 3 ]; then
                /usr/bin/python3 /data/python/oper_instance.py "$node"
                if [ $? -eq 0 ];then
                    rm -f $DIR/${node}_record
                    echo -e "$TIME: $node -> 重启成功\n" >> $DIR/restart_record
                else
                    echo -e "重启实例失败\n" >> $DIR/log_record
                    exit 1
                fi
            else
                echo -e "关键字出现次数为$NUM,本次不进行重启!\n" >> $DIR/${node}_record
            fi
        done
    fi
    wait
}

main
