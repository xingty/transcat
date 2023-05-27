# syntax=docker/dockerfile:1

FROM python:3.10-alpine

ENV TRANSCAT_ASSETS="/var/data/transcat"

WORKDIR /app

COPY requirements.txt setup.py .

RUN  pip3.10 install -r requirements.txt

COPY . .

CMD python flight.py --config /var/data/transcat/config.json