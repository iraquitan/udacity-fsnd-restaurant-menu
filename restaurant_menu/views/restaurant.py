# -*- coding: utf-8 -*-
"""
 * Project: restaurant-menu
 * Author name: Iraquitan Cordeiro Filho
 * Author login: iraquitan
 * File: restaurant
 * Date: 2/17/16
 * Time: 12:18 AM
"""
from restaurant_menu import app
from flask import request, render_template, redirect, abort, flash, url_for, \
    jsonify
from restaurant_menu import db
from restaurant_menu.forms import RestaurantForm
from restaurant_menu.models import Restaurant, MenuItem


# JSON APIs
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurant_menu_json(restaurant_id):
    restaurant = Restaurant.query.filter_by(id=restaurant_id).one()
    items = MenuItem.query.filter_by(restaurant_id=restaurant.id).all()
    return jsonify(menu_items=[i.serialize for i in items])


@app.route('/restaurant/JSON')
def restaurants_json():
    restaurants = Restaurant.query.all()
    return jsonify(restaurants=[r.serialize for r in restaurants])


# Views routes
@app.route('/')
@app.route('/restaurant')
def show_restaurants():
    restaurants = Restaurant.query.all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new', methods=['GET', 'POST'])
def new_restaurant():
    form = RestaurantForm(request.form)
    if form.validate_on_submit():
        new_rest = Restaurant(name=form.name.data)
        db.session.add(new_rest)
        db.session.commit()
        print("Restaurant created!")
        flash("Restaurant created!")
        return "Redirect URL 'restaurants'"
    else:
        return "Render template 'new_restaurant'"


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    restaurant = Restaurant.query.filter_by(id=restaurant_id).one()
    form = RestaurantForm(obj=restaurant)
    if form.validate_on_submit():
        restaurant.name = form.name.data
        db.session.add(restaurant)
        db.session.commit()
        print("Restaurant {} edited!".format((restaurant.id, restaurant.name)))
        flash("Restaurant {} edited!".format((restaurant.id, restaurant.name)))
        return "Redirect URL 'restaurant_menu'"
    else:
        return "Render template 'edit_restaurant'"


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def delete_restaurant(restaurant_id):
    restaurant = Restaurant.query.filter_by(id=restaurant_id)
    if request.form == 'POST':
        db.session.delete(restaurant)
        db.session.commit()
        print("Restaurant {} deleted!".format(
            (restaurant.id, restaurant.name)))
        flash("Restaurant {} deleted!".format(
            (restaurant.id, restaurant.name)))
        return "Redirect URL 'restaurants'"
    else:
        return "Render template 'delete_restaurant'"


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def restaurant_menu(restaurant_id):
    restaurant = Restaurant.query.filter_by(id=restaurant_id).one()
    items = MenuItem.query.filter_by(restaurant_id=restaurant.id).all()
    return render_template('menu.html', restaurant=restaurant, items=items)
