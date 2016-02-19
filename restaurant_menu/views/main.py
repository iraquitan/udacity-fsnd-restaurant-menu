# -*- coding: utf-8 -*-
"""
 * Project: restaurant-menu
 * Author name: Iraquitan Cordeiro Filho
 * Author login: iraquitan
 * File: main
 * Date: 2/18/16
 * Time: 1:13 AM
"""
from flask import render_template, request, flash, make_response
from flask import session as login_session
import random
import string
from restaurant_menu import app, CLIENT_ID, CLIENT_SECRETS_JSON, db

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
        oauth_flow = flow_from_clientsecrets(CLIENT_SECRETS_JSON, scope='')
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
    if result['issued_to'] != CLIENT_ID:
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
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


    # if credentials:
    #     credentials = OAuth2Credentials.from_json(login_session['credentials'])
    #     print('In g_disconnect access token is %s', credentials.access_token)
    #     print("User name is: {}".format(login_session['username']))
    #     # Execute HTTP GET to request revoke of current token
    #     access_token = credentials.access_token
    #     # credentials.revoke(httplib2.Http())
    #     url = "{0}?token={1}".format(credentials.revoke_uri, access_token)
    #     h = httplib2.Http()
    #     result = h.request(url, 'GET')[0]
    #     print("result is {}".format(result))
    #     if result['status'] == '200':
    #         del login_session['credentials']
    #         del login_session['gplus_id']
    #         del login_session['username']
    #         del login_session['email']
    #         del login_session['picture']
    #         response = make_response(
    #             json.dumps('Successfully disconnected.'), 200
    #         )
    #         response.headers['Content-Type'] = 'application/json'
    #         return response
    #     else:
    #         # For whatever reason, the given token was invalid
    #         response = make_response(
    #             json.dumps(
    #                 "Failed to revoke token for given user. Reason: {}".format(
    #                     result.reason
    #                 )),
    #             result.status
    #         )
    #         response.headers['Content-Type'] = 'application/json'
    #         return response
    # else:
    #     print 'Credentials is None'
    #     response = make_response(
    #         json.dumps('Current user not connected.'), 401
    #     )
    #     response.headers['Content-Type'] = 'application/json'
    #     return response
