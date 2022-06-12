#!/usr/bin/env bash
# start virtual env, or install
source .venv/bin/activate || python3.7 -m venv .venv
pip install --upgrade pip && pip install -r requirements.txt

set -a
source .env
set +a

python app.py