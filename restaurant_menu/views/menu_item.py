# -*- coding: utf-8 -*-
"""
 * Project: restaurant-menu
 * Author name: Iraquitan Cordeiro Filho
 * Author login: iraquitan
 * File: menu_item
 * Date: 2/17/16
 * Time: 1:01 AM
"""
from restaurant_menu import app
from flask import request, render_template, redirect, abort, flash, url_for, \
    jsonify
from restaurant_menu import db
from restaurant_menu.forms import MenuItemForm, DeleteForm
from restaurant_menu.models import Restaurant, MenuItem


# JSON APIs
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menu_item_json(restaurant_id, menu_id):
    item = MenuItem.query.filter_by(id=menu_id).one()
    return jsonify(menu_item=item.serialize)


# Views routes
@app.route('/restaurant/<int:restaurant_id>/menu/new/',
           methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
    form = MenuItemForm(request.form)
    restaurant = Restaurant.query.filter_by(id=restaurant_id).one()
    if form.validate_on_submit():
        new_item = MenuItem(name=form.name.data,
                            description=form.description.data,
                            price=form.price.data,
                            course=form.course.data,
                            restaurant_id=restaurant_id)
        db.session.add(new_item)
        db.session.commit()
        if app.debug:
            app.logger.debug("New Menu {} Item Successfully Created".format(
                (new_item.id, new_item.name))
            )
        flash("New Menu {} Item Successfully Created".format(
            (new_item.id, new_item.name))
        )
        return redirect(url_for('restaurant_menu',
                                restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', form=form,
                               restaurant_id=restaurant.id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
    edited_item = MenuItem.query.filter_by(id=menu_id).one()
    form = MenuItemForm(obj=edited_item)
    restaurant = Restaurant.query.filter_by(id=restaurant_id).one()
    if form.validate_on_submit():
        edited_item.name = form.name.data
        edited_item.description = form.description.data
        edited_item.price = form.price.data
        edited_item.course = form.course.data
        db.session.add(edited_item)
        db.session.commit()
        if app.debug:
            app.logger.debug("Menu Item {} Successfully Edited".format(
                (edited_item.id, edited_item.name))
            )
        flash("Menu Item {} Successfully Edited".format(
            (edited_item.id, edited_item.name))
        )
        return redirect(url_for('restaurant_menu',
                                restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', form=form,
                               restaurant_id=restaurant_id, menu_id=menu_id,
                               item=edited_item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_id):
    form = DeleteForm(request.form)
    restaurant = Restaurant.query.filter_by(id=restaurant_id).one()
    item_to_delete = MenuItem.query.filter_by(id=menu_id).one()
    if form.validate_on_submit():
        db.session.delete(item_to_delete)
        db.session.commit()
        if app.debug:
            app.logger.debug("Menu Item {} Successfully Edited".format(
                (item_to_delete.id, item_to_delete.name))
            )
        flash("Menu Item {} Successfully Edited".format(
            (item_to_delete.id, item_to_delete.name))
        )
        return redirect(url_for('restaurant_menu',
                                restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html', form=form,
                               item=item_to_delete,
                               restaurant_id=restaurant_id)
