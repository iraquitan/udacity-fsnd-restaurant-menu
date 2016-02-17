# -*- coding: utf-8 -*-
"""
 * Project: restaurant-menu
 * Author name: Iraquitan Cordeiro Filho
 * Author login: iraquitan
 * File: __init__.py
 * Date: 2/17/16
 * Time: 12:02 AM
"""
from flask import Flask
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config')
app.config.from_pyfile('config.py')
mail = Mail(app)
db = SQLAlchemy(app)
from restaurant_menu.views import restaurant, menu_item
