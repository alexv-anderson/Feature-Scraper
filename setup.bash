#! /bin/bash

python3 -m venv "app"
cd "app"
source ./bin/activate
pip install wheel
pip install scrapy
