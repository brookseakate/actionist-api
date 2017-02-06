# Actionist API
Actionist is an [iOS app](https://github.com/brookseakate/actionist-ios) and REST API created for my Capstone Project at [Ada Developers Academy](http://adadevelopersacademy.org/). Actionist is intended to streamline engagement with social justice and political actions from a mobile device.

From the [iOS App](https://github.com/brookseakate/actionist-ios), Users can retrieve a list of (then act on): Call-, Email-, or Event-type Actions. The Actionist API manages [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) operations for the User, Call Action, Email Action, and Event Action resources.

Learn more about the project at: http://actionistapp.com/

See the iOS app code at: https://github.com/brookseakate/actionist-ios

# Installation
The Actionist API is written in Python using [Flask](http://flask.pocoo.org/).

## Dependencies
### Core Dependencies:
- [Python 2.7.x](https://www.python.org/downloads/)
- [Virtualenv](https://virtualenv.pypa.io/en/stable/)
- [Flask](http://flask.pocoo.org/)
- [Flask-Script](https://flask-script.readthedocs.io/en/latest/)
- [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
- [Flask-RESTful](http://flask-restful-cn.readthedocs.io/en/latest/)
- [Flask-HTTPAuth](https://flask-httpauth.readthedocs.io/en/latest/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

### Database Dependencies (if using Postgres):
- [PostgreSQL](https://www.postgresql.org/)
  - recommended: [Postgres.app](http://postgresapp.com/)
  - recommended: [Postico](https://eggerapps.at/postico/)
- [psycopg2](http://initd.org/psycopg/)

### Etc:
- [Python Faker](https://faker.readthedocs.io/en/latest/) (for seed generator scripts)
- [phonenumbers](https://github.com/daviddrysdale/python-phonenumbers) (for seed generator scripts)
- [less](http://lesscss.org/) (recommended, for index page CSS)

## Getting Started
Before cloning, be sure all necessary packages listed above are installed and executable from your path. Most packages can be installed with [pip](https://pip.pypa.io/en/stable/). (Here are some helpful getting-started guides for [Flask](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) and for [Using PostgreSQL with Flask](http://killtheyak.com/use-postgresql-with-django-flask/).)

Clone the repo:
```
$ git clone <this-repository-url>
$ cd actionist-api
```

## Configuration
Actionist API endpoints require HTTP Basic authentication. Assign a username and password for authorized HTTP requests. The application also needs to know your database path.

Define the following environment variables in a `.env` file at the project root:

```python
# .env

HTTP_AUTH_PASSWORD = "password"

HTTP_AUTH_USERNAME = "username"

SQLALCHEMY_DATABASE_URI = "database://your/database/URI"
# see sample db URI formats here: http://flask-sqlalchemy.pocoo.org/2.1/config/#configuration-keys
```

## Running for Development
To run the application locally:
```
$ source venv/bin/activate
$ python application.py
```
When launched successfully, the application logs will confirm the local server's IP:
```
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
You can now make requests against your local server.

## Seeding the Database
To populate your database using the included seed generator scripts, run `python manage.py dbseed` with the `-c` flag to specify a quantity.

For example, to seed 10 each of Users, Call Actions, Email Actions, and Event Actions, run:
```
$ python manage.py dbseed -c 10
```

# Usage
All responses are provided in JSON format.

## Authenticating API requests
Actionist API endpoints require HTTP Basic authentication. Include your username and password with each request.

## REST Endpoints
NOTE: When running locally, `<yourserver>` will be `localhost:5000` unless otherwise specified.

### Base URI:
```
http://<yourserver>/api/v1.0/
```
### Actions:
```
http://<yourserver>/api/v1.0/actions/
```
- GET: Retrieve a list of all Actions (Call, Email, or Event)

### Call Actions:
```
http://<yourserver>/api/v1.0/call_actions/
```
- GET: Retrieve a list of all Call Actions
- POST: Create a new Call Action

```
http://<yourserver>/api/v1.0/call_actions/<id>
```
- GET: Retrieve the specified Call Action
- PUT: Update the specified Call Action
- DELETE: Delete the specified Call Action

### Email Actions:
```
http://<yourserver>/api/v1.0/email_actions/
```
- GET: Retrieve a list of all Email Actions
- POST: Create a new Email Action

```
http://<yourserver>/api/v1.0/email_actions/<id>
```
- GET: Retrieve the specified Email Action
- PUT: Update the specified Email Action
- DELETE: Delete the specified Email Action

### Event Actions:
```
http://<yourserver>/api/v1.0/event_actions/
```
- GET: Retrieve a list of all Event Actions
- POST: Create a new Event Action

```
http://<yourserver>/api/v1.0/event_actions/<id>
```
- GET: Retrieve the specified Event Action
- PUT: Update the specified Event Action
- DELETE: Delete the specified Event Action

### Users:
```
http://<yourserver>/api/v1.0/users/
```
- GET: Retrieve a list of all Users
- POST: Create a new User

```
http://<yourserver>/api/v1.0/users/<id>
```
- GET: Retrieve the specified User
- PUT: Update the specified User
- DELETE: Delete the specified User

## Sample Curl Requests
These sample requests run against a default local server (`localhost:5000`). Substitute your server location if running on a different host.

- Get a list of all Actions:
```
curl -i -H "Content-Type: application/json" -X GET http://localhost:5000/api/v1.0/actions -u username:password
```

- Create a new User:
```
curl -i -H "Content-Type: application/json" -X POST -d '{ "user_name": "lunarox", "first_name": "Luna", "last_name": "Lovegood", "about": "Spells and outer space", "zip": "98101" }' http://localhost:5000/api/v1.0/users -u username:password
```

- Update a Call Action:
```
curl -i -H "Content-Type: application/json" -X PUT -d '{ "target_phone_number": "2065551212" }' http://localhost:5000/api/v1.0/call_actions/1 -u username:password
```

- Delete an Event Action:
```
curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/api/v1.0/event_actions/123 -u username:password
```

## Resource Relationships and Parameters
For more information about API resources and parameters, see the [Actionist ERD](ERD_Actionist_API.pdf).

# Links
- [Ada Developers Academy Website](http://adadevelopersacademy.org/)
- [Actionist App Website](https://actionistapp.com)
- [Actionist iOS Code](https://github.com/brookseakate/actionist-ios)
- [My Website](http://kateshaffer.com)
- App Icon & Favicon: [Protest by Chris Kerr from the Noun Project](https://thenounproject.com/term/fist/15242)
- Bootstrap Theme (index page):
[New Age](https://startbootstrap.com/template-overviews/new-age/)
