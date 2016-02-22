# -*- coding: utf-8 -*-
"""
 * Project: restaurant-menu
 * Author name: Iraquitan Cordeiro Filho
 * Author login: iraquitan
 * File: __init__.py
 * Date: 2/17/16
 * Time: 12:02 AM
"""
import json
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__, instance_relative_config=True)

GOOGLE_CLIENT_SECRETS_JSON = "../restaurant-menu/instance/client_secrets.json"
GOOGLE_CLIENT_ID = json.loads(
    open(GOOGLE_CLIENT_SECRETS_JSON, 'r').read()
)['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"

FACEBOOK_CLIENT_SECRETS_JSON = "../restaurant-menu/instance/fb_client_secrets.json"
FACEBOOK_CLIENT_SECRETS = json.loads(
    open(FACEBOOK_CLIENT_SECRETS_JSON, 'r').read()
)['web']

app.config.from_object('config')
app.config.from_pyfile('config.py')
mail = Mail(app)
db = SQLAlchemy(app)
if app.debug:
    log_file_handler = RotatingFileHandler(
        '../restaurant-menu/restaurant_menu/basic-logging.txt',
        maxBytes=10000, backupCount=0)
    app.logger.addHandler(log_file_handler)
from restaurant_menu.views import main, restaurant, menu_item
