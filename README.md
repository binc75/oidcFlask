## OpenID Connect Playground
Little POC about OpenID Connect and OAuth 2.0 using KeyCloak and Python3

## Setup
### KeyCloak
Firt of all we need to install an OIDC (OpenID Connect) server (Identity Provider).

For convenience we will use KeyCloak in a Docker container.
Here below the necessary steps to setup our IdP:

```bash
docker run -p 8080:8080 --name kc-idp \
  -e KC_BOOTSTRAP_ADMIN_USERNAME=user \
  -e KC_BOOTSTRAP_ADMIN_PASSWORD=password \
  -e DB_VENDOR=H2 \
  -d keycloak/keycloak start-dev
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
docker cp keycloak-setup.sh kc-idp:/opt/keycloak/keycloak-setup.sh
docker exec kc-idp /opt/keycloak/keycloak-setup.sh 
# you can ignore the output of the above script execution, it will be fine ;-)

# Get secret TOKEN for client
export APP_TOKEN=$(docker exec kc-idp /opt/keycloak/bin/kcreg.sh get mypyapp --realm master --server http://localhost:8080 --user user --password password | jq -r '.secret')
```

### Create app configuration file
```bash
cat client_secrets-template.json | envsubst > client_secrets.json 
```

Create a new user for testing
```bash
docker exec kc-idp /opt/keycloak/bin/kcadm.sh create users --server http://localhost:8080 --realm master --user user --password password -s username=nbianchi  -s enabled=true
docker exec kc-idp /opt/keycloak/bin/kcadm.sh set-password --username nbianchi --new-password abc123 --server http://localhost:8080 --realm master --user user --password password 
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
