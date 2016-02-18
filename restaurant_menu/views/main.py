# -*- coding: utf-8 -*-
"""
 * Project: restaurant-menu
 * Author name: Iraquitan Cordeiro Filho
 * Author login: iraquitan
 * File: main
 * Date: 2/18/16
 * Time: 1:13 AM
"""
from flask import session as login_session, render_template
import random
import string

from restaurant_menu import app


# Create anti-forgery state token
@app.route('/login')
def show_login():
    state = ''.join(random.choice(
        string.ascii_uppercase + string.digits + string.ascii_lowercase)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html')
