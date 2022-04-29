#FROM alpine:3.5
FROM python:3.7.13-slim
#RUN apk add --update python py-pip

WORKDIR /src

COPY . ./
#COPY requirements.txt ./
#COPY main.py ./
#COPY buzz ./
#COPY modules ./
#COPY civil-hash.json ./key/

RUN pwd && ls -la && pip3 install -r requirements.txt

CMD python main.py
