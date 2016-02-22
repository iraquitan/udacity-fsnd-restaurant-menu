# -*- coding: utf-8 -*-
"""
 * Project: restaurant-menu
 * Author name: Iraquitan Cordeiro Filho
 * Author login: iraquitan
 * File: restaurant
 * Date: 2/17/16
 * Time: 12:18 AM
"""
import json

from restaurant_menu import app
from flask import request, render_template, redirect, abort, flash, url_for, \
    jsonify, make_response
from flask import session as login_session
from restaurant_menu import db
from restaurant_menu.forms import RestaurantForm, DeleteForm
from restaurant_menu.models import User, Restaurant, MenuItem
from restaurant_menu.views.main import get_user_info


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
    username = login_session.get('username')
    if username is None:
        return render_template('publicrestaurants.html',
                               restaurants=restaurants)
    else:
        return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new', methods=['GET', 'POST'])
def new_restaurant():
    username = login_session.get('username')
    if username is None:
        return redirect('/login')
    form = RestaurantForm(request.form)
    if form.validate_on_submit():
        new_rest = Restaurant(name=form.name.data,
                              user_id=login_session['user_id'])
        db.session.add(new_rest)
        db.session.commit()
        if app.debug:
            app.logger.debug("Restaurant {} added!".format((new_rest.id,
                                                            new_rest.name)))
        flash("Restaurant {} added!".format((new_rest.id, new_rest.name)))
        return redirect(url_for('show_restaurants'))
    else:
        return render_template('new_restaurant.html', form=form)


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    username = login_session.get('username')
    if username is None:
        return redirect('/login')
    restaurant = Restaurant.query.filter_by(id=restaurant_id).one()
    # Check if the current user is the creator
    if login_session.get('user_id') != restaurant.user_id:
        return "<script>function myFunction() {" \
               "alert('You are not authorized to edit this restaurant. " \
               "Please create your own restaurant in order to edit.');" \
               "}</script><body onload='myFunction()'>"
    form = RestaurantForm(obj=restaurant)
    if form.validate_on_submit():
        restaurant.name = form.name.data
        db.session.add(restaurant)
        db.session.commit()
        if app.debug:
            app.logger.debug("Restaurant {} edited!".format((restaurant.id,
                                                             restaurant.name)))
        flash("Restaurant {} edited!".format((restaurant.id, restaurant.name)))
        return redirect(url_for('restaurant_menu',
                                restaurant_id=restaurant_id))
    else:
        return render_template('editrestaurant.html', form=form,
                               restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def delete_restaurant(restaurant_id):
    username = login_session.get('username')
    if username is None:
        return redirect('/login')
    form = DeleteForm(request.form)
    restaurant = Restaurant.query.filter_by(id=restaurant_id).one()
    # Check if the current user is the creator
    if login_session.get('user_id') != restaurant.user_id:
        return "<script>function myFunction() {" \
               "alert('You are not authorized to delete this restaurant. " \
               "Please create your own restaurant in order to delete.');" \
               "}</script><body onload='myFunction()'>"
    if form.validate_on_submit():
        db.session.delete(restaurant)
        db.session.commit()
        if app.debug:
            app.logger.debug("Restaurant {} deleted!".format(
                (restaurant.id, restaurant.name)))
        flash("Restaurant {} deleted!".format(
            (restaurant.id, restaurant.name)))
        return redirect(url_for('show_restaurants'))
    else:
        return render_template('deleterestaurant.html', form=form,
                               restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def restaurant_menu(restaurant_id):
    restaurant = Restaurant.query.filter_by(id=restaurant_id).one()
    creator = get_user_info(restaurant.user_id)
    items = MenuItem.query.filter_by(restaurant_id=restaurant.id).all()
    if login_session.get('user_id') == creator.id:
        return render_template('menu.html', restaurant=restaurant, items=items,
                               creator=creator)
    else:
        return render_template('publicmenu.html', restaurant=restaurant,
                               items=items, creator=creator)
