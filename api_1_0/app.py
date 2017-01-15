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
from resources.user import UserListAPI, UserAPI
from resources.call_action import CallActionListAPI, CallActionAPI
from resources.email_action import EmailActionListAPI, EmailActionAPI
from resources.event_action import EventActionListAPI, EventActionAPI

# # @TODO - remove, unneeded
# from models import User, CallAction, EmailAction, EventAction

# register routes
api.add_resource(UserListAPI, '/api/v1.0/users', endpoint = 'users')
api.add_resource(UserAPI, '/api/v1.0/users/<int:id>', endpoint = 'user')
api.add_resource(CallActionListAPI, '/api/v1.0/call_actions', endpoint = 'call_actions')
api.add_resource(CallActionAPI, '/api/v1.0/call_actions/<int:id>', endpoint = 'call_action')
api.add_resource(EmailActionListAPI, '/api/v1.0/email_actions', endpoint = 'email_actions')
api.add_resource(EmailActionAPI, '/api/v1.0/email_actions/<int:id>', endpoint = 'email_action')
api.add_resource(EventActionListAPI, '/api/v1.0/event_actions', endpoint = 'event_actions')
api.add_resource(EventActionAPI, '/api/v1.0/event_actions/<int:id>', endpoint = 'event_action')
