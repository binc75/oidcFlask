#!/bin/sh

cd /

# User creation in the master realm
/opt/keycloak/bin/kcreg.sh config credentials \
  --server http://localhost:8080/auth \
  --realm master \
  --user user \
  --password password \
  --client admin-cli

# Create the configuraition for the client app
/opt/keycloak/bin/kcreg.sh create \
  --server http://localhost:8080/ \
  --realm master \
  --user user \
  --password password \
  --client admin-cli \
  -s clientId="mypyapp" \
  -s 'redirectUris=["http://localhost:5000/*", "http://127.0.0.1:5000/*"]' \
  -s secret='test-secret-key'

# Check the conf and get back the secret for the client app
/opt/keycloak/bin/kcreg.sh get "mypyapp" --server http://localhost:8080/auth --realm master --user user --password password | grep '"secret"'

