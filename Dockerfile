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
