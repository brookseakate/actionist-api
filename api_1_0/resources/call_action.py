# package imports
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, reqparse, fields, marshal

# relative imports
from ..models import CallAction
# from ..models import User # likely to need this...
# from ..models import CRUD, CallAction # @TODO - remove

# from ../..app import app, db
# # @TODO - remove
# # App setup
# app = Flask(__name__)
# app.config.from_pyfile('../../config.py')
# db = SQLAlchemy(app)

# public field definitions (for use with marshal)
# @TODO - update to send detailed user info rather than just user_id?
call_action_public_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'headline': fields.String,
    'description': fields.String,
    'list_start_datetime': fields.DateTime,
    'list_end_datetime': fields.DateTime,
    'target_phone_number': fields.String,
    'target_name': fields.String,
    'target_official_type': fields.String,
    'script': fields.String,
    'talking_point_1': fields.String,
    'talking_point_2': fields.String,
    'talking_point_3': fields.String,
    'kudos_text': fields.String,
    'uri': fields.Url('call_action', absolute=True),
    # @TODO: use below version for https!
    # 'uri': fields.Url('call_action', absolute=True, scheme='https')
    'user_id': fields.String
    # # @TODO - add user_uri?
    # 'user_uri': field.Url('user', absolute=True)
}

# define resources, routes, and argument validation
class CallActionListAPI(Resource):
    def __init__(self):
        # @TODO - figure out datetime handling, see http://stackoverflow.com/questions/26662702/what-is-the-datetime-format-for-flask-restful-parser
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, required = True, help = 'A title is required', location = 'json')
        self.reqparse.add_argument('headline', type = str, location = 'json')
        self.reqparse.add_argument('description', type = str, location = 'json')
        self.reqparse.add_argument('list_start_datetime', type = str, location = 'json')
        self.reqparse.add_argument('list_end_datetime', type = str, location = 'json')
        self.reqparse.add_argument('target_phone_number', type = str, location = 'json')
        self.reqparse.add_argument('target_name', type = str, location = 'json')
        self.reqparse.add_argument('target_official_type', type = str, location = 'json')
        self.reqparse.add_argument('script', type = str, location = 'json')
        self.reqparse.add_argument('talking_point_1', type = str, location = 'json')
        self.reqparse.add_argument('talking_point_2', type = str, location = 'json')
        self.reqparse.add_argument('talking_point_3', type = str, location = 'json')
        self.reqparse.add_argument('kudos_text', type = str, location = 'json')
        self.reqparse.add_argument('user_id', type = str, location = 'json')
        self.reqparse.add_argument('zip', type = str, location = 'json')

        super(CallActionListAPI, self).__init__()

    def get(self):
        call_actions_query = CallAction.query.all()
        return { 'call_actions': [marshal(call_action, call_action_public_fields) for call_action in call_actions] }

    def post(self):
        try:
            args = self.reqparse.parse_args()
            new_call_action = CallAction(
                title = args['title'],
                headline = args['headline'],
                description = args['description'],
                list_start_datetime = args['list_start_datetime'],
                list_end_datetime = args['list_end_datetime'],
                target_phone_number = args['target_phone_number'],
                target_name = args['target_name'],
                target_official_type = args['target_official_type'],
                script = args['script'],
                talking_point_1 = args['talking_point_1'],
                talking_point_2 = args['talking_point_2'],
                talking_point_3 = args['talking_point_3'],
                kudos_text = args['kudos_text'],
                user_id = args['user_id'] # this might need to reference the user instance itself
            )
            new_call_action.add(new_call_action)
            # or could set new_call_action.user(User.query.get(['user_id']))
            return { 'call_action': marshal(new_call_action, call_action_public_fields) }, 201
        # @TODO - fix error handling here (session not rolling back properly. Also clobbering validation errors into generic 400s)
        except Exception as err:
            db.session.rollback()
            resp = jsonify({"error": str(err)})
            resp.status_code = 403
            return resp

class CallActionAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, location = 'json')
        self.reqparse.add_argument('headline', type = str, location = 'json')
        self.reqparse.add_argument('description', type = str, location = 'json')
        self.reqparse.add_argument('list_start_datetime', type = str, location = 'json')
        self.reqparse.add_argument('list_end_datetime', type = str, location = 'json')
        self.reqparse.add_argument('target_phone_number', type = str, location = 'json')
        self.reqparse.add_argument('target_name', type = str, location = 'json')
        self.reqparse.add_argument('target_official_type', type = str, location = 'json')
        self.reqparse.add_argument('script', type = str, location = 'json')
        self.reqparse.add_argument('talking_point_1', type = str, location = 'json')
        self.reqparse.add_argument('talking_point_2', type = str, location = 'json')
        self.reqparse.add_argument('talking_point_3', type = str, location = 'json')
        self.reqparse.add_argument('kudos_text', type = str, location = 'json')
        self.reqparse.add_argument('user_id', type = str, location = 'json')
        self.reqparse.add_argument('zip', type = str, location = 'json')

        super(CallActionAPI, self).__init__()

    def get(self, id):
        call_action = CallAction.query.get_or_404(id)
        return { 'call_action': marshal(call_action, call_action_public_fields) }

    def put(self, id):
        # @TODO - add error handling (see POST)
        call_action = CallAction.query.get_or_404(id)
        args = self.reqparse.parse_args()
        for k, v in args.iteritems():
            if v != None:
                setattr(call_action, k, v)
        call_action.update()
        return self.get(id)

    def delete(self, id):
        call_action = CallAction.query.get_or_404(id)
        call_action.delete(call_action)
        return { 'result': True }
