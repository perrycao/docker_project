# -*- coding:utf-8 -*-
# version 0.1 2019-05-03 First update
import json
import time
import atexit
import logging
import argparse
import requests
import schedule
from kafka import KafkaProducer
from kafka.errors import KafkaError, KafkaTimeoutError

logger_format = "%(asctime)s - %(message)s"
logging.basicConfig(format=logger_format)
logger = logging.getLogger("data_producer")
logger.setLevel(logging.DEBUG)

API_BASE = "https://api.gdax.com"


def check_symbol(_symbol):
    """
    helper method to check if the symbol exits in coinbase API
    """
    logger.debug("Checking symbol.")
    try:
        response = requests.get(API_BASE + '/products')
        product_ids = [product['id'] for product in response.json()]
        if _symbol not in product_ids:
            logger.warning("Symbol %s not supported. The list of supported symbols: %s", _symbol, product_ids)
            exit()
    except Exception as e:
        logger.warning("Failed to fetch products.", e)
        exit()


def fetch_price(_symbol, _topic_name, _producer):
    """
    helper method to retrieve data and send it to kafka.
    """
    logger.debug("Start to fetch data for %s", _symbol)
    try:
        response = requests.get(f"{API_BASE}/products/{_symbol}/ticker")
        price = response.json()['price']
        timestamp = time.time()
        payload = {
            "Symbol": str(_symbol),
            "LastTradePrice": str(price),
            "Timestamp": str(timestamp)
        }
        logger.debug("Retrieved %s info %s", _symbol, payload)
        byte_value = json.dumps(payload).encode("utf-8")
        _producer.send(topic=_topic_name, value=byte_value, timestamp_ms=int(time.time() * 1000))
    except KafkaTimeoutError as timeout_error:
        logger.warning("Failed to send message to kafka, caused by: %s", timeout_error)
    except Exception as e:
        logger.warning("Failed to fetch price: %s", e)


def shutdown_hook(_producer):
    """
    helper method to clean up response when shutting down
    """
    try:
        _producer.flush(10)
    except KafkaError as kafka_error:
        logger.warning("Failed to flush pending message, caused by: %s", kafka_error)
    finally:
        try:
            _producer.close(10)
        except Exception as e:
            logger.warning("Failed to close kafka connection, caused by: %s", e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("symbol", help='the symbol you want to pull.')
    parser.add_argument("topic_name", help="the kafka topic push to.")
    parser.add_argument("kafka_broker", help="the location of kafka broker.")

    # Parse arguments
    args = parser.parse_args()
    symbol = args.symbol
    topic_name = args.topic_name
    kafka_broker = args.kafka_broker

    # Check if the symbol is supported
    check_symbol(symbol)

    # Instantiate a simple kafka producer
    producer = KafkaProducer(bootstrap_servers=kafka_broker)

    # Schedule and run fetch_price function every second
    schedule.every(1).second.do(fetch_price, symbol, topic_name, producer)

    # Setup proper shutdown hook
    atexit.register(shutdown_hook, producer)

    while True:
        schedule.run_pending()
