#! /usr/bin/env python
#coding=utf-8
from pykafka import KafkaClient

client = KafkaClient(hosts="1.1.1.1:80")

def produce_kafka_data(kafka_topic):
        with kafka_topic.get_sync_producer() as producer:
		producer.produce('This is alive')

def consume_simple_kafka(kafka_topic, timeout):
        consumer = kafka_topic.get_simple_consumer(consumer_group='Kafka_Zabbix_Host', consumer_id='Kafka_Zabbix_Host_1', consumer_timeout_ms=timeout)
        count = 0
        for message in consumer:
                if message is not None:
                        #print message.offset, message.value
                        count += 1
        with open('/tmp/zabbix_kafka','w+') as f:
                f.write(str(count))
        #print count

if __name__ == '__main__':
        try:
                topic = client.topics["Zabbix_Monitor"]
                #produce_kafka_data(topic)
                consume_simple_kafka(topic,1000)
        except:
                with open('/tmp/zabbix_kafka','w+') as f:
                        f.write('0')
