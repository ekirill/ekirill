FROM python:3.8.3-buster

RUN apt-get update \
    && apt-get install -y \
        iproute2 \
    && true
RUN pip install --upgrade pip

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

COPY src/ /app/
WORKDIR /app/
