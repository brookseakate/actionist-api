# package imports
from flask import Flask, make_response, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_httpauth import HTTPBasicAuth

# App setup
application = Flask(__name__)
application.config.from_pyfile('../config.py')
db = SQLAlchemy(application)
api = Api(application)
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'authentikate':
        return application.config['HTTP_AUTH_PASSWORD']
    return None

@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
    return make_response( jsonify( {'message': 'Unauthorized access'} ), 403)

# relative imports
from resources.user import UserListAPI, UserAPI
from resources.call_action import CallActionListAPI, CallActionAPI
from resources.email_action import EmailActionListAPI, EmailActionAPI
from resources.event_action import EventActionListAPI, EventActionAPI
from resources.action import ActionListAPI
from resources.health import HealthAPI

# register index route
@application.route('/')
def index():
    return render_template('index.html')

# register routes
api.add_resource(UserListAPI, '/api/v1.0/users', endpoint = 'users')
api.add_resource(UserAPI, '/api/v1.0/users/<int:id>', endpoint = 'user')
api.add_resource(CallActionListAPI, '/api/v1.0/call_actions', endpoint = 'call_actions')
api.add_resource(CallActionAPI, '/api/v1.0/call_actions/<int:id>', endpoint = 'call_action')
api.add_resource(EmailActionListAPI, '/api/v1.0/email_actions', endpoint = 'email_actions')
api.add_resource(EmailActionAPI, '/api/v1.0/email_actions/<int:id>', endpoint = 'email_action')
api.add_resource(EventActionListAPI, '/api/v1.0/event_actions', endpoint = 'event_actions')
api.add_resource(EventActionAPI, '/api/v1.0/event_actions/<int:id>', endpoint = 'event_action')
api.add_resource(ActionListAPI, '/api/v1.0/actions', endpoint = 'actions')
api.add_resource(HealthAPI, '/health', endpoint = 'health') # NOTE: 200 OK for Elastic Beanstalk pings
