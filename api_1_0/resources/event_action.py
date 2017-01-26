# package imports
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, reqparse, fields, marshal

# relative imports
from ..app import db, auth
from ..models import EventAction

# public field definitions (for use with marshal)
# @TODO - update to require user_id on creation (line 45), & set user relationship on action (line 69)
event_action_public_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'headline': fields.String,
    'description': fields.String,
    'list_start_datetime': fields.DateTime(dt_format='iso8601'),
    'list_end_datetime': fields.DateTime(dt_format='iso8601'),
    'location': fields.String,
    'event_start_datetime': fields.DateTime(dt_format='iso8601'),
    'event_end_datetime': fields.DateTime(dt_format='iso8601'),
    'kudos_text': fields.String,
    'uri': fields.Url('event_action', absolute=True, scheme='https'),
    'user_id': fields.Integer
    # # @TODO - add user_uri?
    # 'user_uri': field.Url('user', absolute=True)
}

# define resources, routes, and argument validation
class EventActionListAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, required = True, help = 'A title is required', location = 'json')
        self.reqparse.add_argument('headline', type = str, location = 'json')
        self.reqparse.add_argument('description', type = str, location = 'json')
        self.reqparse.add_argument('list_start_datetime', type = str, location = 'json')
        self.reqparse.add_argument('list_end_datetime', type = str, location = 'json')
        self.reqparse.add_argument('location', type = str, location = 'json')
        self.reqparse.add_argument('event_start_datetime', type = str, location = 'json')
        self.reqparse.add_argument('event_end_datetime', type = str, location = 'json')
        self.reqparse.add_argument('kudos_text', type = str, location = 'json')
        self.reqparse.add_argument('user_id', type = int, location = 'json')

        super(EventActionListAPI, self).__init__()

    def get(self):
        event_actions_query = EventAction.query.all()
        return { 'event_actions': [marshal(event_action, event_action_public_fields) for event_action in event_actions_query] }

    def post(self):
        try:
            args = self.reqparse.parse_args()
            new_event_action = EventAction(
                title = args['title'],
                headline = args['headline'],
                description = args['description'],
                list_start_datetime = args['list_start_datetime'],
                list_end_datetime = args['list_end_datetime'],
                location = args['location'],
                event_start_datetime = args['event_start_datetime'],
                event_end_datetime = args['event_end_datetime'],
                kudos_text = args['kudos_text'],
                user_id = args['user_id'] # this might need to reference the user instance itself
            )
            new_event_action.add(new_event_action)
            # or could set new_event_action.user(User.query.get(['user_id']))
            return { 'event_action': marshal(new_event_action, event_action_public_fields) }, 201

        except Exception as err:
            db.session.rollback()
            resp = jsonify({"error": str(err)})
            resp.status_code = 403
            return resp

class EventActionAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, location = 'json')
        self.reqparse.add_argument('headline', type = str, location = 'json')
        self.reqparse.add_argument('description', type = str, location = 'json')
        self.reqparse.add_argument('list_start_datetime', type = str, location = 'json')
        self.reqparse.add_argument('list_end_datetime', type = str, location = 'json')
        self.reqparse.add_argument('location', type = str, location = 'json')
        self.reqparse.add_argument('event_start_datetime', type = str, location = 'json')
        self.reqparse.add_argument('event_end_datetime', type = str, location = 'json')
        self.reqparse.add_argument('kudos_text', type = str, location = 'json')
        self.reqparse.add_argument('user_id', type = int, location = 'json')

        super(EventActionAPI, self).__init__()

    def get(self, id):
        event_action = EventAction.query.get_or_404(id)
        return { 'event_action': marshal(event_action, event_action_public_fields) }

    def put(self, id):
        event_action = EventAction.query.get_or_404(id)
        args = self.reqparse.parse_args()
        for k, v in args.iteritems():
            if v != None:
                setattr(event_action, k, v)
        event_action.update()
        return self.get(id)

    def delete(self, id):
        event_action = EventAction.query.get_or_404(id)
        event_action.delete(event_action)
        return { 'result': True }
