# -*- coding: utf-8 -*-
"""
 * Created by PyCharm.
 * Project: restaurant-menu
 * Author name: Iraquitan Cordeiro Filho
 * Author login: pma007
 * File: database_setup
 * Date: 1/26/16
 * Time: 17:20
 * To change this template use File | Settings | File Templates.
"""
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)


class MenuItem(Base):
    __tablename__ = 'menu_item'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

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
            'price': self.price
        }

# Insert at end of file
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
