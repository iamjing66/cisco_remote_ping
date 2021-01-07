#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from kafka import KafkaProducer


class Kafka_producer:
    """
    生产模块：根据不同的key，区分消息
    """

    def __init__(self, kafkabroker, kafkatopic):
        self.kafkabroker = kafkabroker
        self.kafkatopic = kafkatopic
        self.producer = KafkaProducer(bootstrap_servers=self.kafkabroker, api_version=(0, 10))

    def sendjsondata(self, params):
        producer = self.producer
        data = json.dumps(params)
        producer.send(topic=self.kafkatopic, key=None, value=data)
        producer.flush()


def kafka_producer(mes):
    KAFKA_SERVERS = ['172.30.26.211:9093','172.30.26.212:9093','172.30.26.213:9093']
    producer = Kafka_producer(KAFKA_SERVERS, "Remote_ping_test")
    producer.sendjsondata(mes)

