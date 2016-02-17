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
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Regexp, Optional


class RestaurantForm(Form):
    name = StringField('Restaurant name', [
        InputRequired(message='Restaurant name is required')])


class DeleteForm(Form):
    delete = SubmitField('Delete')


class MenuItemForm(Form):
    name = StringField('Menu item name', [
        InputRequired(message='Menu item name is required')])
    course = SelectField('Course',
                         choices=[('Entree', 'Entree'),
                                  ('Appetizer', 'Appetizer'),
                                  ('Dessert', 'Dessert'),
                                  ('Beverage', 'Beverage')
                                  ])
    description = TextAreaField('Description', validators=[Optional()])
    # price = DecimalField('Item price', [NumberRange(
    #     min=0, message='Must 0 or positive'), Optional()])
    price = StringField('Item price', [
        Regexp('^((\$)|(R\$)|(\xA3)){1}\d{0,8}(\.\d{1,2})?$',
               message='Not a valid price value. '
                       'Must start with dollar, pound or br-real sign '
                       'and only 2 decimals')])
