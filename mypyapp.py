#!/usr/bin/env python3

#
#
# OIDC OAuth2 POC
# Library used: https://flask-oidc.readthedocs.io/en/latest/
#
#


# Imports
import requests
import json
import jwt
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_oidc import OpenIDConnect
from oauth2client.client import OAuth2Credentials



# Initialize Flask app
app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'PartiallySecret',
    'TESTING': True,
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    'OIDC_USER_INFO_ENABLED': True,
    'OIDC_OPENID_REALM': 'master',
    'OIDC_SCOPES': ['openid', 'email', 'profile'],
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post'
})


# Initialize OpenIDConnect
oidc = OpenIDConnect(app)


# Routes
## landing page
@app.route('/')
def app_route():
    '''Landing page'''

    if oidc.user_loggedin:
        message = 'Hi {}! You are logged in'.format(oidc.user_getfield('preferred_username'))
        return render_template('index.html', message=message)
    else:
        message = 'Not logged in yet!'
        return render_template('index.html', message=message, login=True)



## Protected / Login page
@app.route('/login')
@oidc.require_login
def login():
    '''Login page: this redirect to keycloak if not yet logged in, then
       print details of the user gathered form the the IdP
    '''

    info = oidc.user_getinfo(['preferred_username', 'email', 'sub',])

    username = info.get('preferred_username')
    email = info.get('email')
    user_id = info.get('sub')
    scopes = OAuth2Credentials.from_json(oidc.credentials_store[user_id]).scopes
    access_token = ''
    jwt_token = ''


    if user_id in oidc.credentials_store:
        try:
            access_token = OAuth2Credentials.from_json(oidc.credentials_store[user_id]).access_token # extract access token
            jwt_token = OAuth2Credentials.from_json(oidc.credentials_store[user_id]).id_token_jwt # extract jwt token
        except:
            print("Can not extract token info")

    # decode jwt
    jwt_data = jwt.decode(jwt_token, app.config['SECRET_KEY'], verify=False, algorithms=['HS256'])
    print(jwt_data)

    # Dictinary to pass to the rendered page
    data = {"username": username, "e-mail": email, "userId": user_id, "scopes": scopes, "access_token": str(access_token), "jwt": jwt_data}

    # Generating curl string to pass to the rendered page
    curl_string = 'curl -s -H "Content-Type: application/json" -H "Authorization: Bearer {}" http://localhost:5000/api'.format(access_token)

    return render_template('login.html', username=username, data=data, curl=curl_string)


## REST API endpoint
@app.route('/api', methods=['GET', 'POST'])
@oidc.accept_token(require_token=True, scopes_required=['openid'])
def api():
    '''OAuth 2.0 protected API endpoint accessible w/ AccessToken'''

    return jsonify({'message': 'Welcome to the protected API'})


## Logout
@app.route('/logout')
def logout():
    '''Performs local logout by removing the session cookie.'''

    oidc.logout()
    return redirect(url_for('app_route'))


# Initialize main app
if __name__ == '__main__':
        app.run(host='0.0.0.0',port='5000', debug=True)

