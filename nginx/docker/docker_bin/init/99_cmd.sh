#!/bin/bash

set -ex

if [ $# -eq 0 ]
then
    echo "Staring nginx"
    chown -R www-data /var/www/webdav/
    htpasswd -bc /etc/nginx/htpasswd $EKIRILL_WEBDAV_LOGIN $EKIRILL_WEBDAV_PASSWORD
    exec /usr/sbin/nginx -g "daemon off;"
else
    exec $@
fi
