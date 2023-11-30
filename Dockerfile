FROM python:3.10.13

ENV PYTHONUNBUFFERED=1

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY ./StockTaking/ /app/
COPY ./setup_files/configfile /app/StockTaking/config.ini 