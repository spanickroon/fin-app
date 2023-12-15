FROM python:3.12-slim

RUN apt-get update; \
	apt-get install -y --no-install-recommends;

RUN apt-get install g++ libqpdf-dev -y
RUN apt install gettext -y

COPY requirements.txt /

RUN pip3 install --upgrade pip; \
    pip3 install -r /requirements.txt

COPY . /src
WORKDIR /src

EXPOSE 8000
