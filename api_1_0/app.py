# package imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

# App setup
app = Flask(__name__)
app.config.from_pyfile('../config.py')
db = SQLAlchemy(app)
api = Api(app)

# relative imports
# from ..models import User, CallAction, EmailAction, EventAction
# # @TODO - remove, unneeded
# from ..models import CRUD, User, CallAction, EmailAction, EventAction
from resources.user import UserListAPI, UserAPI
from resources.call_action import CallActionListAPI, CallActionAPI

# # @TODO - uncomment once created
# from ..resources.email_action import EmailActionListAPI, EmailActionAPI
# from ..resources.event_action import EventActionListAPI, EventActionAPI

# register routes
api.add_resource(UserListAPI, '/api/v1.0/users', endpoint = 'users')
api.add_resource(UserAPI, '/api/v1.0/users/<int:id>', endpoint = 'user')
api.add_resource(CallActionListAPI, '/api/v1.0/users', endpoint = 'call_actions')
api.add_resource(CallActionAPI, '/api/v1.0/users/<int:id>', endpoint = 'call_action')

# # @TODO - remove once created
# api.add_resource(EmailActionListAPI, '/api/v1.0/users', endpoint = 'email_actions')
# api.add_resource(EmailActionAPI, '/api/v1.0/users/<int:id>', endpoint = 'email_action')
# api.add_resource(EventActionListAPI, '/api/v1.0/users', endpoint = 'event_actions')
# api.add_resource(EventActionAPI, '/api/v1.0/users/<int:id>', endpoint = 'event_action')

# create/update database to match SQLAlchemy models
db.create_all()

# # @TODO - comment out! this drops the test databases
# db.drop_all()

# # make file executable if main
# if __name__ == '__main__':
#     app.run(debug=True)
