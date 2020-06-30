FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y \
        apache2-utils \
        build-essential \
        ffmpeg \
        python3 \
        python3-dev \
        python3-pip \
        nginx-full \
    && true

RUN mkdir /tmp/upload/ \
    && mkdir /var/www/webdav/ \
    && chown -R www-data /tmp/upload/ \
    && rm -rf /etc/nginx/sites-enabled/* \
    && true

COPY docker/conf/*.nginx /etc/nginx/modules-enabled/
COPY docker/conf/conf.d/*.nginx /etc/nginx/conf.d/
COPY docker/conf/sites-enabled/*.nginx /etc/nginx/sites-enabled/

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

COPY docker/docker_bin /docker_bin
RUN chmod +x /docker_bin/*.sh \
    && chmod +x /docker_bin/init/*.sh \
    && true
ENTRYPOINT ["/docker_bin/entrypoint.sh"]

COPY src/ /app/
WORKDIR /app/
