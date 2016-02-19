# -*- coding: utf-8 -*-
"""
 * Project: restaurant-menu
 * Author name: Iraquitan Cordeiro Filho
 * Author login: iraquitan
 * File: models
 * Date: 2/17/16
 * Time: 12:06 AM
"""
from restaurant_menu import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    picture = db.Column(db.String(250))

    @property
    def serialize(self):
        """
        Returns object data in easily serializable format
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture
        }


class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)

    @property
    def serialize(self):
        """
        Returns object data in easily serializable format
        """
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id
        }


class MenuItem(db.Model):
    __tablename__ = 'menu_item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    course = db.Column(db.String(250))
    description = db.Column(db.String(250))
    price = db.Column(db.String(8))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    restaurant = db.relationship(Restaurant)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)

    @property
    def serialize(self):
        """
        Returns object data in easily serializable format
        """
        return {
            'id': self.id,
            'name': self.name,
            'course': self.course,
            'description': self.description,
            'price': self.price,
            'restaurant_id': self.restaurant_id,
            'user_id': self.user_id
        }
