#FROM alpine:3.5
FROM python:3.7.12-slim
#RUN apk add --update python py-pip

WORKDIR /src

COPY . ./

RUN pip3 install -r requirements.txt && locale-gen en_US.UTF-8

ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU:en
ENV LC_ALL ru_RU.UTF-8

CMD python main.py
