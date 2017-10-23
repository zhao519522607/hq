#! /usr/bin/env python
# -*- coding:utf-8 -*-
from kafka import KafkaProducer
from kafka import KafkaConsumer

def producer_main():
    producer = KafkaProducer(bootstrap_servers=['1.1.1.1:80'], client_id='Zabbix_Host')
    for i in range(200):
        producer.send('Zabbix_Test', b'This alive %s' %str(i ** 2))
    producer.flush()

def consumer_main():
    consumer = KafkaConsumer('Zabbix_Test', bootstrap_servers=['1.1.1.1:80'], group_id='Kafka_Zabbix_Host', client_id='Kafka_Zabbix_Host_129')
    count = 0
    for message in consumer:
        if message:
	    print message.offset, message.value
            count += 1
    #with open('/tmp/zabbix_kafka','w+') as f:
    #    f.write(str(count))

if __name__ == '__main__':
    #try:
    #    producer_main()
    #    consumer_main()
    #except:
    #    with open('/tmp/zabbix_kafka','w+') as f:
    #        f.write('0')
    producer_main()
    consumer_main()
