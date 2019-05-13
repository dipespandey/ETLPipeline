'''The app module, containing the app factory function.'''

import os

from flask import Flask
from flask_cors import CORS

from routes import routes

from config import ProdConfig, DevConfig

if os.getenv("FLASK_ENV") == 'prod':
    DefaultConfig = ProdConfig
else:
    DefaultConfig = DevConfig


def create_app(config_object=DefaultConfig):
    '''An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/
    :param config_object: The configuration object to use.
    '''
    app = Flask(__name__)
    register_blueprints(app)
    CORS(app, origins=[],
         headers=['Content-Type'], expose_headers='Access-Control-Allow-Origin')
    return app


def register_blueprints(app):
    app.register_blueprint(routes)


# def register_cors(app):
#     CORS(app, resources={r"*": {"origins": "*"}})
