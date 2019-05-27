import json
import argparse
import atexit
import happybase
import logging

from kafka import KafkaConsumer
from kafka.errors import KafkaError


logger_format = '%(asctime)s - %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('data_storage')
logger.setLevel(logging.DEBUG)


def shutdown_hook(_consumer, _hbase_connection):
    """
    a shutdown hook to be called before the shutdown.
    """
    try:
        logger.info('Closing Kafka consumer.')
        _consumer.close()
        logger.info('Kafka consumer closed.')
        logger.info('Closing hbase connection.')
        _hbase_connection.close()
        logger.info('hbase connection closed.')
    except KafkaError as kafka_error:
        logger.warning(f'Failed to close Kafka consumer, caused by: {kafka_error}')
    finally:
        logger.info('Exiting program.')


def persist_data(data, _hbase_connection, _data_table):
    # TODO
    """
    persist data into hbase.
    """
    try:
        logger.debug(f'Start to persist data to hbase: {data}')
        parsed = json.load(data)
        symbol = parsed.get('Symbol')
        price = float(parsed.get('LastTradePrice'))
        timestamp = parsed.get('Timestamp')

        table = _hbase_connection.table(_data_table)
        row_key = f"{symbol}-{timestamp}"
        logger.info(f'String data values with row key: {row_key}')
        row_value = {
            'family:symbol': str(symbol),
            'family:trade_time': str(timestamp),
            'family:trade_price': str(price)
        }
        table.put(row_key, row_value)
        logger.debug(f'Persisted data to hbase for symbol: {symbol}, price: {price}, timestamp: {timestamp}')
    except Exception as e:
        logger.error(f'Failed to persist data to hbase for {e}')


if __name__ == '__main__':
    # Setup command line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument('topic_name', help='the kafka topic to subscribe from.')
    parser.add_argument('kafka_broker', help='the location of the kafka broker.')
    parser.add_argument('data_table', help='the data table to use.')
    parser.add_argument('hbase_host', help='the host name of hbase.')

    # Parse arguments.
    args = parser.parse_args()
    topic_name = args.topic_name
    kafka_broker = args.kafka_broker
    data_table = args.data_table
    hbase_host = args.hbase_host

    # Initiate a simple kafka consumer.
    consumer = KafkaConsumer(topic_name, bootstrap_server=kafka_broker)

    # Initiate a hbase connection
    hbase_connection = happybase.Connection(hbase_host)

    # Create table is not exists.
    if data_table not in hbase_connection.tables():
        hbase_connection.create_table(data_table, {'family': dict()})

    # Setup proper shutdown hook.
    atexit.register(shutdown_hook, consumer, hbase_connection)

    for msg in consumer:
        persist_data(msg.value, hbase_connection, data_table)
