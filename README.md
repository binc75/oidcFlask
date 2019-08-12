## OpenID Connect Playground
Little POC about OpenID Connect and OAuth 2.0 written in python3

## Setup
### KeyCloak
Firt of all we need to install an OIDC (OpenID Connect) server (Identity Provider).

For convenience we will use KeyCloak in a Docker container.
Here below the necessary steps to setup our IdP:

```bash
docker run -p 8080:8080 --name kc-idp \
  -e KEYCLOAK_USER=user \
  -e KEYCLOAK_PASSWORD=password \
  -e DB_VENDOR=H2 \
  -d jboss/keycloak
```

Check if KeyCloak is up&running
```bash
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
7c7b2d8b513a        jboss/keycloak      "/opt/jboss/tools/do…"   7 seconds ago       Up 5 seconds        0.0.0.0:7777->8080/tcp   kc-idp
```

Now that KeyCloak is up and running we will configure the client (our python app)
Create a file called **keycloak-setup.sh** with the following content:
``` bash
#!/bin/sh

# User creation in the master realm
keycloak/bin/kcreg.sh config credentials \
  --server http://localhost:8080/auth \
  --realm master \
  --user user \
  --password password

# Create the configuraition for the client app
keycloak/bin/kcreg.sh create \
  --server http://localhost:8080/auth \
  --realm master \
  -s clientId="mypyapp" \
  -s 'redirectUris=["http://localhost:5000/*", "http://127.0.0.1:5000"]'

# Check the conf and get back the secret for the client app
keycloak/bin/kcreg.sh get "mypyapp" --server http://localhost:8080/auth  --realm master | jq '.secret'
```

Now we need to copy the script to the Docker container and run it
``` bash
docker cp keycloak-setup.sh kc-idp:/opt/jboss/keycloak-setup.sh
docker exec kc-idp chmod 750 /opt/jboss/keycloak-setup.sh
docker exec kc-idp /opt/jboss/keycloak-setup.sh
```
Keep note of the output returned, this must be used in the **client_secret.json** file
(ie. 7747b4ea-e877-40c6-a987-2de6c931d52c)

Create a new user for testing
```bash
docker exec kc-idp /opt/jboss/keycloak/bin/add-user-keycloak.sh -u nbianchi -p abc123 -r master
docker restart kc-idp
```

### Flask app setup
Create virtualenv
```bash

python3 -m venv env
source env/bin/activate
pip install -r requirements.txt --no-cache

```
