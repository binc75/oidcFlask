#!/usr/bin/env python3

#
# Add KeyCloak user via RestAPI
#

import requests
import json

# Get Admin token
payload = { 'username': 'user', 'password': 'password', 'grant_type': 'password', 'client_id': 'admin-cli'}
resp = requests.post('http://localhost:8080/auth/realms/master/protocol/openid-connect/token', data=payload)
token = resp.json()['access_token']


# Create user
headers = {'Content-Type': 'application/json', 'Authorization': 'bearer {}'.format(token)}
payload = {
            "firstName":"Pinco",
            "lastName":"Pallino", 
            "email":"pincopallino@gmail.com", 
            "enabled":"true", 
            "username": "ppallino", 
            "credentials":[{"type":"password","value":"test1"}]
          }

resp = requests.post('http://localhost:8080/auth/admin/realms/master/users', data=json.dumps(payload), headers=headers)

if resp.status_code == 201:
    print('User succesfully created!')
else:
    print('No able to create user')
