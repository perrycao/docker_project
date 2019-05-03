# docker_project
TDU class project for practicing docker kafka.

## Dockerfile
```dockerfile
# Docker image containing data_product and data_consumer.

FROM ubuntu:latest
MAINTAINER Perry Cao "perrycao2015@gmail.com"

RUN apt-get update
RUN apt-get install -y python python-pip wget
COPY ./data_producer.py /
COPY ./data_consumer.py /
COPY ./requirements.txt /
RUN pip install -r requirements.txt

CMD python data-producer.py BTC-USD test kafka:9092
```

## Run docker images
```
docker run -d -p 2181:2181 -p 2888:2888 -p 3888:3888 --name zookeeper confluent/zookeeper
docker run -d -p 9092:9092 -e KAFKA_ADVERTISED_HOST_NAME=localhost -e KAFKA_ADVERTISED_PORT=9092 --name kafka --link zookeeper:zookeeper confluent/kafka
```

## Run data_producer.py
```
python src\data_producer.py BTC-USD test 127.0.0.1:9092
```

## Run data_consumer.py
```
python src\data_consumer.py test 127.0.0.1:9092
```

## Setup environment
### requirements.txt
```
pip install -r requirements.txt
```