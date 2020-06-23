#!/bin/bash

set -ex

for f in /docker_bin/init/*; do
    ${f} $@
done
