#!/usr/bin/env bash
set -ex

HOST_DOMAIN="host.docker.internal"

HOST_IP=$(ip route | awk 'NR==1 {print $3}')
echo -e "$HOST_IP\t$HOST_DOMAIN" >> /etc/hosts


echo "Waiting postgres to launch on ${EKIRILL_WEB_DB_HOST}:5432..."
while ! nc -z ${EKIRILL_WEB_DB_HOST} 5432; do
  sleep 1
done
echo "postgres launched"


exec "$@"
