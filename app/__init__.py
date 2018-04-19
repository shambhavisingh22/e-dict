from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from flask import Flask
import lib.log as log
import logging
from config import config, APP_NAME
from elasticsearch import *
Logger = logging.getLogger(APP_NAME)

Logger = logging.getLogger(APP_NAME)

db = SQLAlchemy()
es = Elasticsearch()

def initialize_db(app):
    db.init_app(app)
    migrate = Migrate(app, db)


def create_app(config_name):
    app = Flask(__name__)
    CORS(app,resources={r"":{"origins":""}})
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    log.setup_logging(config[config_name])

    initialize_db(app)


    from app.dictionary.views import dict as global_router
    app.register_blueprint(global_router, url_prefix='/words')

    return app
