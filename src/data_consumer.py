# -*- coding:utf-8 -*-
# version 0.1 2019-05-03 First update
import argparse
from kafka import KafkaConsumer


def consume(_topic_name, _kafka_broker):
    """
    helper method to consume certain topic data from kafka broker
    """
    consumer = KafkaConsumer(_topic_name, bootstrap_servers=_kafka_broker)

    for message in consumer:
        print(message)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("topic_name", help="the kafka topic to pull from.")
    parser.add_argument("kafka_broker", help="the location of kafka broker.")

    # Parse arguments
    args = parser.parse_args()
    topic_name = args.topic_name
    kafka_broker = args.kafka_broker

    # Consume topic
    consume(topic_name, kafka_broker)
