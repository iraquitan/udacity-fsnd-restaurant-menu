# -*- coding: utf-8 -*-
"""
 * Created by PyCharm.
 * Project: restaurant-menu
 * Author name: Iraquitan Cordeiro Filho
 * Author login: pma007
 * File: project
 * Date: 2/4/16
 * Time: 16:01
 * To change this template use File | Settings | File Templates.
"""
from flask import Flask, render_template, request, url_for, redirect, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurant_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)


# Task 1: Create route for new_menu_item function here
@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
    if request.method == 'POST':
        if request.form['name']:
            name = request.form['name']
        else:
            raise AttributeError("name must not be null!")
        if request.form['description']:
            description = request.form['description']
        else:
            description = None
        if request.form['price']:
            price = request.form['price']
        else:
            price = None
        if request.form['course']:
            course = request.form['course']
        else:
            course = None
        new_item = MenuItem(name=name,
                            restaurant_id=restaurant_id,
                            description=description, price=price,
                            course=course)
        session.add(new_item)
        session.commit()
        flash("New menu item created!")
        return redirect(url_for('restaurant_menu',
                                restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


# Task 2: Create route for edit_menu_item function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['price']:
            item.price = request.form['price']
        if request.form['course']:
            item.course = request.form['course']
        session.add(item)
        session.commit()
        flash("Menu item edited!")
        return redirect(url_for('restaurant_menu',
                                restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html',
                               restaurant_id=restaurant_id,
                               menu_id=menu_id, item=item)


# Task 3: Create a route for delete_menu_item function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Menu item deleted!")
        return redirect(url_for('restaurant_menu',
                                restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html',
                               restaurant_id=restaurant_id,
                               menu_id=menu_id, item=item)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
