# -*- coding: utf-8 -*-
"""
 * Project: restaurant-menu
 * Author name: Iraquitan Cordeiro Filho
 * Author login: iraquitan
 * File: forms
 * Date: 2/17/16
 * Time: 12:06 AM
"""
from flask_wtf import Form
from wtforms import StringField, FloatField, DateField, SelectField, \
    TextAreaField, FormField, IntegerField, DecimalField, SelectMultipleField
from wtforms.fields.html5 import URLField
from wtforms.validators import url, InputRequired, Regexp, NumberRange, \
    Optional, Email


class RestaurantForm(Form):
    name = StringField('Restaurant name', [
        InputRequired(message='Restaurant name is required')])


class MenuItemForm(Form):
    name = StringField('Menu item name', [
        InputRequired(message='Menu item name is required')])
    course = SelectField('Course',
                         choices=[('entree', 'Entree'),
                                  ('appetizer', 'Appetizer'),
                                  ('dessert', 'Dessert'),
                                  ('beverage', 'Beverage')
                                  ])
    description = TextAreaField('Description', validators=[Optional()])
    price = DecimalField('Item price', [
        NumberRange(min=0, message='Must 0 or positive'), Optional()])
