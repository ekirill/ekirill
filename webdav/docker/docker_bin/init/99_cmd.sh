#!/bin/bash

if [ $# -eq 0 ]
then
  echo "Staring storage size watcher"
  exec python3 -u /app/size_watcher.py
else
  exec $@
fi
