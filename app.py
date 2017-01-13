# package imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

# relative imports
from api_1_0.models.models import *
from api_1_0.user import *

# App setup
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
api = Api(app)

# register routes
api.add_resource(UserListAPI, '/api/v1.0/users', endpoint = 'users')
api.add_resource(UserAPI, '/api/v1.0/users/<int:id>', endpoint = 'user')

# create/update database to match SQLAlchemy models
db.create_all()

# # @TODO - comment out! this drops the test databases
# db.drop_all()

# make file executable if main
if __name__ == '__main__':
    app.run(debug=True)
