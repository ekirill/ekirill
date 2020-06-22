FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y \
        apache2-utils \
        build-essential \
        python3 \
        python3-dev \
        python3-pip \
        nginx-full \
    && mkdir /tmp/upload/ \
    && true

COPY docker/nginx/webdav.nginx /etc/nginx/nginx.conf

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

COPY docker/docker_bin /docker_bin
RUN chmod +x /docker_bin/*.sh \
    && chmod +x /docker_bin/init/*.sh \
    && true
ENTRYPOINT /docker_bin/entrypoint.sh

COPY src/ /app/
WORKDIR /app/
