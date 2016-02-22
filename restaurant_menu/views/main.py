# -*- coding: utf-8 -*-
"""
 * Project: restaurant-menu
 * Author name: Iraquitan Cordeiro Filho
 * Author login: iraquitan
 * File: main
 * Date: 2/18/16
 * Time: 1:13 AM
"""
from flask import render_template, request, flash, make_response, redirect, \
    url_for
from flask import session as login_session
import random
import string
from restaurant_menu import app, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRETS_JSON,\
    db, FACEBOOK_CLIENT_SECRETS

# IMPORTS FOR THIS STEP
from oauth2client.client import flow_from_clientsecrets, OAuth2Credentials
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

from restaurant_menu.models import User


def create_user(login_session):
    new_user = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    db.session.add(new_user)
    db.session.commit()
    user = User.query.filter_by(email=login_session['email']).one()
    return user.id


def get_user_info(user_id):
    user = User.query.filter_by(id=user_id).one()
    return user


def get_user_id(email):
    try:
        user = User.query.filter_by(email=email).one()
        return user.id
    except:
        return None


# Create anti-forgery state token
@app.route('/login')
def show_login():
    state = ''.join(random.choice(
        string.ascii_uppercase + string.digits + string.ascii_lowercase)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def g_connect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(GOOGLE_CLIENT_SECRETS_JSON,
                                             scope='')
        oauth_flow.redirect_uri = 'postmessage'
        # oauth_flow.step1_get_authorize_url()
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    # Check that the access token is valid.
    url = ("{0}?access_token={1}".format(credentials.token_info_uri,
                                         access_token))
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != GOOGLE_CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401
        )
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200
        )
        response.headers['Content-Type'] = 'application/json'
        flash("Welcome back {}".format(login_session['username']))
        return response

    # Store the access token in the session for later use.
    login_session['provider'] = 'google'
    login_session['credentials'] = credentials.to_json()
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Create a new user in database if user does not exist
    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '  # noqa
    flash("You are now logged in as {}".format(login_session['username']))
    print "done!"
    return output


@app.route('/gdisconnect')
def g_disconnect():
    """Revoke current user's token and reset their session."""
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    credentials = OAuth2Credentials.from_json(login_session['credentials'])
    # Execute HTTP GET to request revoke of current token
    access_token = credentials.access_token
    # credentials.revoke(httplib2.Http())
    url = "{0}?token={1}".format(credentials.revoke_uri, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's session.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/fbconnect', methods=['POST'])
def fb_connect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    short_access_token = request.data
    app_id = FACEBOOK_CLIENT_SECRETS['app_id']
    app_secret = FACEBOOK_CLIENT_SECRETS['app_secret']
    url = "https://graph.facebook.com/v2.5/oauth/access_token?" \
          "grant_type=fb_exchange_token&client_id={0}&client_secret={1}" \
          "&fb_exchange_token={2}".format(app_id, app_secret,
                                          short_access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    userinfo_url = "https://graph.facebook.com/v2.5/me?&access_token={0}" \
                   "&fields=name,id,email"
    long_access_token = json.loads(result)['access_token']
    url = userinfo_url.format(long_access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['facebook_id'] = data['id']
    # Get user picture
    userpicture_url = "https://graph.facebook.com/v2.5/me/picture?" \
                      "&access_token={0}&redirect=0&height=200&width=200"
    url = userpicture_url.format(long_access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['picture'] = data['data']['url']
    # Create a new user in database if user does not exist
    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '  # noqa
    flash("You are now logged in as {}".format(login_session['username']))
    print "done!"
    return output


@app.route('/fbdisconnect', methods=['POST'])
def fb_disconnect():
    facebook_id = login_session['facebook_id']
    url = "https://graph.facebook.com/{0}/permissions".format(facebook_id)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    del login_session['facebook_id']
    return "You have been logged out"


@app.route('/disconnect', methods=['POST'])
def disconnect():
    provider = login_session.get('provider')
    if provider:
        if provider == 'google':
            g_disconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if provider == 'facebook':
            fb_disconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash('You have successfully been logged out.')
        return redirect(url_for('show_restaurants'))
    else:
        flash('You were not logged in to begin with!')
        return redirect(url_for('show_restaurants'))
