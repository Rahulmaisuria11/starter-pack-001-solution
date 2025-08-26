## Software required:

- Bruno or Postman for API Testing
- Some IDE, like Pycharm or Visual Studio Code
- Git
- Docker desktop or some VM where you can run this code.

## Accounts needed:

- Github

## Required Environment Variables:

### pgadmin
````
PGADMIN_DEFAULT_EMAIL
PGADMIN_DEFAULT_PASSWORD
PGADMIN_PORT
````

### postgres
````
POSTGRES_PASSWORD
POSTGRES_DB
POSTGRES_USER
POSTGRES_INITDB_ARGS
````

### api
````
TESTING=true
SECRET_KEY
POSTGRESQL_USERNAME
POSTGRESQL_PASSWORD
POSTGRESQL_HOST
POSTGRESQL_PORT
POSTGRESQL_DB
POSTGRESQL_ARGS
````

## Documentation:

- https://flask.palletsprojects.com/en/3.0.x/
- https://flask-sqlalchemy.palletsprojects.com/en/2.x/
  - I am currently using version 2.x, but feel free to check the newest.
- https://docs.docker.com/develop/
- https://jinja.palletsprojects.com/en/3.1.x/
  - for template creation

## Flask Application

### Tree
````python
|   .env
|   app.py
|   config.py
|   diagram.png
|   Dockerfile
|   requirements.txt
|   starter-pack-001.db
|   tree.txt
|   
+---app
|   |   __init__.py
|   |   
|   +---models
|   |   |   engineer.py
|   |   |   location.py
|   |   |   roles.py
|   |   |   roles_secondary.py
|   |   |   __init__.py
|   |   |   
|   |           
|   +---static
|   |   \---css
|   |           styles.css
|   |           
|   +---templates
|   |       index.html
|   |       
|   +---utils
|   |   |   starter-pack-001_Bruno_API.json
|   |   |   starter-pack-001_Postman_API.json
|   |   |   
|   |   \---starter-pack-001
|   |       |   bruno.json
|   |       |   
|   |       +---Engineers
|   |       |       Delete Engineer.bru
|   |       |       Engineer.bru
|   |       |       Engineers.bru
|   |       |       New Engineer.bru
|   |       |       Update Engineer.bru
|   |       |       
|   |       +---environments
|   |       +---Locations
|   |       |       Delete Location.bru
|   |       |       Location.bru
|   |       |       Locations.bru
|   |       |       New Location.bru
|   |       |       Update Location.bru
|   |       |       
|   |       \---Roles
|   |               Delete Role.bru
|   |               New Role.bru
|   |               Role.bru
|   |               Roles.bru
|   |               Update Role.bru
|   |               
|           
+---migrations
|   |   alembic.ini
|   |   env.py
|   |   README
|   |   script.py.mako
|   |   
|   +---versions
|
````

### Models:

````python
Engineer
Location
Roles
RolesSecondary
````

#### Some notes:
- An Engineer can be the custodian of multiple Locations -> One-to-Many
- An Engineer can be assigned to multiple Roles and vice-versa -> Many-to-Many
- RolesSecondary table is required for the Many-to-Many relationship models to work

### SQL Diagram with tables

![SQL Diagram](/api/diagram.png "San Juan Mountains")

## Useful commands:

create your virtual environment
````python
python -m venv .venv
````

activate your virtual environment
````
.\.venv\Scripts\activate
````

install your dependencies
````python
pip install -r .\api\requirements.txt
````

run your python server locally
````
python api\app.py
````

build your api service and then run run your services in compose.yaml
using the **--watch** flag will allow you to rebuild them when changes are made.
###### don't forget to create a **.venv** file in the root folder
````
docker compose build --no-cache api
docker compose --env-file ".env" up --watch
````
