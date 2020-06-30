#!/bin/bash

set -ex

if [ $# -eq 0 ]
then
    echo "Staring storage size watcher"
    python3 -u /app/thumb_maker.py
fi
