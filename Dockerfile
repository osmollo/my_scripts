FROM python:3.8-alpine

WORKDIR /scripts
COPY requirements.txt /scripts

RUN apk add --no-cache --virtual build-deps libffi-dev gcc build-base python3-dev py-configobj libusb linux-headers libc-dev musl-dev tzdata\
    && apk add --no-cache --update vim bash py-pip jq less curl \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && rm -f /scripts/requirements.txt \
    && cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime \
    && apk del build-deps

COPY *py /scripts/

ENTRYPOINT [ "python" ]
