FROM ubuntu:18.04

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /home/user/

RUN apt-get update  \ 
    && apt-get install -y git python3 python3-pip libmariadbclient-dev

RUN git clone https://github.com/HighHopesInt/products_aggregator.git -b release-fix

WORKDIR /home/user/products_aggregator/

COPY .env ./

RUN pip3 install -r requirements.txt
