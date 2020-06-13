#!/usr/bin/env bash

project_dir="$(cd "$(dirname "$0")/.." && pwd)"
app_dir="$project_dir/back/src"
(cd $app_dir && uvicorn  ekirill.app:app --reload --workers 2 --limit-concurrency 5 --port 8176)
