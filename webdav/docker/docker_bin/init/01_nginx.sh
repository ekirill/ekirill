#!/bin/bash

set -e

if [ $# -eq 0 ]
then
    echo "Staring nginx"
    htpasswd -bc /etc/nginx/htpasswd $EKIRILL_WEBDAV_LOGIN $EKIRILL_WEBDAV_PASSWORD
    exec /usr/sbin/nginx -g "daemon on; master_process on;"
fi
