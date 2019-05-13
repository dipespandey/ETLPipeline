#!/usr/bin/python3
import sys
import os
import logging
logging.basicConfig(stream=sys.stderr)

activate_this = '/var/www/etl-api-new/venv/bin/activate_this.py'
with open(activate_this) as file_:
        exec(file_.read(), dict(__file__=activate_this))
path = 'var/www/etl-api-new/app'

sys.path.insert(0, path)

from __init__ import create_app
application = create_app()
