
# E-COMMERCE API'S

REST API using Python and hosting it locally using Docker and using MongoDB as the database.

## CONFIGURATION

* INSTALLING requirements.txt
* CREATING API's IN PYTHON FILE
* INITIALIZING THE DATABASE.js FILE
* PROVIDING CONFIGURATION DOCKER FILE
* DOCKER COMPOSE FILE FOR LINKING MULTIPLE CONTAINERS

### INSTALLING requirements.txt

* Installing the required modules Flask and Flask-PyMongo

### CREATING API's IN PYTHON FILE

* Importing libraries
* Creating a flask Server and connecting with MongoDB
* Defining CRUD methods and routes( ADD-PRODCT, GET-PRODUCTS, DELETE-PRODUCTS, UPDATE-PRODUCTS )
* BONUS ROUTES
* Defining error handlers
* Initializing the driver code

### INITIALIZING THE DATABASE.js FILE

* Providing the DB Name and Collection to initialize the db with given document of 5000 items

### PROVIDING CONFIGURATION DOCKER FILE

* Select python image
* Adding everything to the working docker directory
* Installing requirements

### DOCKER COMPOSE FILE FOR LINKING MULTIPLE CONTAINERS

* Docker-Compose file allows us to link multiple containers and run them at the same time. In our code we are linking two containers i.e. Mongo Image and the Main Application

## DEPLOYMENT

To deploy this project run

```bash
  docker-compose up
```