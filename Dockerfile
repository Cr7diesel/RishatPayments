FROM python:3.10-alpine3.19

ENV PYTHONUNBUFFERED=1

WORKDIR /payments

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN apk add postgresql-client build-base postgresql-dev
RUN pip install -r requirements.txt
RUN adduser --disabled-password admin


USER admin

COPY . /payments

EXPOSE 8000