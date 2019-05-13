#!/bin/bash

cd /var/www/etl-api-new/
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements/prod.txt
