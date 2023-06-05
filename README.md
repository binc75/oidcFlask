## OpenID Connect Playground
Little POC about OpenID Connect and OAuth 2.0 using KeyCloak and Python3

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

Now we will configure the client (our python app) into KeyCloak  
We need to copy the script to the Docker container and run it
``` bash
git clone git@github.com:binc75/oidcFlask.git
cd oidcFlask/
docker cp keycloak-setup.sh kc-idp:/opt/jboss/keycloak-setup.sh
docker exec kc-idp /opt/jboss/keycloak-setup.sh

# Get secret TOKEN for client
export APP_TOKEN=$(docker exec kc-idp /opt/jboss/keycloak/bin/kcreg.sh get "mypyapp" --server http://localhost:8080/auth  --realm master | jq -r '.secret')
```

### Create app configuration file
```bash
cat client_secrets-template.json | envsubst > client_secrets.json 
```

Create a new user for testing
```bash
docker exec kc-idp /opt/jboss/keycloak/bin/add-user-keycloak.sh -u nbianchi -p abc123 -r master
docker restart kc-idp
```
...alternatively you can also use the script **kc_user_add.py**

### Flask app setup
Create virtualenv
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt --no-cache
./mypyapp.py
```
...go and visit http://localhost:5000 ! 

(user: nbianchi, pass: abc123 or user: ppallino, pass:test1 if you used the script **kc_user_add.py**)

### Get Autorization server public key 
...to validate JWT on jwt.io
```bash
curl -s http://localhost:8080/auth/realms/master/ | jq -r .public_key
```
