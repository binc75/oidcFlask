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
chmod 755 keycloak-setup.sh
docker cp keycloak-setup.sh kc-idp:/opt/jboss/keycloak-setup.sh
docker exec kc-idp /opt/jboss/keycloak-setup.sh
```
---

**NOTE**
Keep note of the output returned, this must be used in the **client_secret.json** file
(ie. 7747b4ea-e877-40c6-a987-2de6c931d52c)

---
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
