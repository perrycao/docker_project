import argparse
import atexit
import logging
import json
import time

from kafka import KafkaProducer
from kafka.errors import KafkaError, KafkaTimeoutError
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


logger_format = "%(asctime)s - %(message)%"
logging.basicConfig(format=logger_format)
logger = logging.getLogger('data_stream')
logger.setLevel(logging.DEBUG)


def process_stream(stream, kafka_producer, target_topic):
    """
    """
    def pair(data):
        record = json.loads(data.decode('utf-8'))
        return record.get('Symbol'), (float(record.get('LastTradePrice')), 1)

    def send_to_kafka(rdd):
        results = rdd.collect()
        for r in results:
            data = json.dumps({
                "Symbol": r[0],
                "Timestamp": time.time(),
                "Average": r[1]
            })

            try:
                logger.info(f"Sending average price {data} to kafka.")
                kafka_producer.send(target_topic, value=data)
            except KafkaError as kafka_error:
                logger.warning(f'Failed to send average price to kafka, caused by {kafka_error}')
        pass

    stream.map(pair).reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1])).map(
        lambda (k, v): (k, v[0] / v[1])).foreachRDD(send_to_kafka)
    pass


def shutdown_hook(producer: KafkaProducer):
    """
    a shutdown hook to be called before the shutdown
    """
    try:
        logger.info("Flushing pending message to kafka, timeout is set to 10s.")
        producer.flush(10)
        logger.info("Flushed flushing pending message to kafka")
    except KafkaError as kafka_error:
        logger.warning(f"Flushed to flush pending message to kafka, caused by: {kafka_error}")
    finally:
        try:
            logger.info("Closing kafka connection.")
            producer.close()
        except Exception as e:
            logger.warning(f"Failed to close kafka connection, caused by {e}")


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
    ssc = StreamingContext(sc, batch_duration)

    # Instantiate kafka stream for processing
    directKafkaStream = KafkaUtils.createDirectStream(ssc, [source_topic], {'metadata.broker.list': kafka_broker})

    # Extract value from directKafkaStream pair
    stream = directKafkaStream.map(lambda  x: x[1])

    # Instantiate a simple kafka producer
    kafka_producer = KafkaProducer(bootstrap_servers=kafka_broker)

    process_stream(stream, kafka_producer, target_topic)

    # Setup proper shutdown hook
    atexit.register(shutdown_hook, kafka_producer)

    ssc.start()
    ssc.awaitTermination()
