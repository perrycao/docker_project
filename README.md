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

## Docker image
```
docker run -d -h myhbase -p 2181:2181 -p 8080:8080 -p 8085:8085 -p 9090:9090 -p 9095:9095 -p 16000:16000 -p 16201:16201 -p 16301:16301 --name hbase harisekhon/hbase
docker run -d -p 9092:9092 -e KAFKA_ADVERTISED_HOST_NAME=localhost -e KAFKA_ADVERTISED_PORT=9092 --name kafka --link hbase:zookeeper confluent/kafka
```

## into hbase shell
```
docker exec -it <container name> <executable file location>
docker exec -it hbase /bin/bash
```

## Run data_storage.py
```
python src\data_storage.py test 127.0.0.1:9092 cryptocurrency myhbase
```

## Run data_stream.py
> 查看这个资源
> https://edu.talkingdata.com/mine/class/cfca876f-36f0-4fca-bbd5-62830fcadf34/%E5%88%86%E6%9E%90%E6%B5%81%E6%95%B0%E6%8D%AE/Spark%E4%BB%A3%E7%A0%81%E5%AE%9E%E6%88%98/spark%E4%BB%A3%E7%A0%81%E5%AE%9E%E6%88%98
> 36:09
```
spark-submit --jars spark-streaming-kafka-0-8-assembly_2.11-2.0.0.jar data_stream.py analyzer Average 127.0.0.1:9092 5
```

## Run docker image
```
docker run -d -p 6379:6379 --name redis redis:alpine
```


## Run redis_publisher.py
- install redis
    - https://github.com/rgl/redis/downloads
```
python src\redis_publisher.py analyzer 127.0.0.1:9092 price 127.0.0.1 6379
```

```
docker exec -it redis redis-cli
```


## 2019-06-25 note
```
docker run -d -p 2181:2181 -p 2888:2888 -p 3888:3888 --name zookeeper confluent/zookeeper
docker run -d -p 9092:9092 -e KAFKA_ADVERTISED_HOST_NAME=localhost -e KAFKA_ADVERTISED_PORT=9092 --name kafka --link zookeeper:zookeeper confluent/kafka
docker run -d -p 6379:6379 --name redis redis:alpine

python src/data_producer.py BTC-USD analyzer 127.0.0.1:9092
python src/redis_publisher.py analyzer 127.0.0.1:9092 Average 127.0.0.1 6379
docker exec -it redis redis-cli
subscribe Average
node -v
npm -v
cd node
npm init --yes
npm install socket.io --save
npm install express
npm install redis
npm install jquery
npm install minimist
npm install bootstrap
npm install d3@3.5.17
npm install nvd3


? -> spark-submit --jar spark-streaming-kafka-0-8-assembly_2.11-2.0.0.jar
```