import argparse
import atexit
import logging
import json

from kafka import KafkaProducer
from kafka.errors import KafkaError, KafkaTimeoutError
from pys


logger_format = "%(asctime)s - %(message)%"
logging.basicConfig(format=logger_format)
logger = logging.getLogger('data_stream')
logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    # Setup command line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument('source_topic', help='the kafka topic to subscribe from.')
    parser.add_argument('target_topic', help='the kafka topic to send data to.')
    parser.add_argument('kafka_broker', help='the broker of kafka.')
    parser.add_argument('batch_duration', help='the batch duration in secs.')

    # Parse arguments.
    args = parser.parse_args()
    source_topic = args.source_topic
    target_topic = args.target_topic
    kafka_broker = args.kafka_broker
    batch_duration = int(args.batch_duration)

    # create spark context and streaming context
    sc = SparkContext('local[2]', 'AveragePrice')
    sc.setLogLevel("INFO")
    ssc = StreamingContext(sc, bactch_duration)

    # Instantiate kafka stream for processing
    directKafkaStream = KafkaUtils.createDirectStream(ssc, [source_topic], {'metadata.broker.list': kafka_broker})