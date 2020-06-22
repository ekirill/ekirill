#!/bin/bash

for f in /docker_bin/init/*; do
    ${f} "$@"
done
