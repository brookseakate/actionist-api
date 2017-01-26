# package imports
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, reqparse, fields, marshal

# relative imports
from ..app import db, auth
from ..models import EmailAction

# public field definitions (for use with marshal)
# @TODO - update to require user_id on creation (line 53), & set user relationship on action (line 82)
email_action_public_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'headline': fields.String,
    'description': fields.String,
    'list_start_datetime': fields.DateTime(dt_format='iso8601'),
    'list_end_datetime': fields.DateTime(dt_format='iso8601'),
    'target_email': fields.String,
    'target_name': fields.String,
    'target_official_type': fields.String,
    'email_subject': fields.String,
    'email_body': fields.String(attribute='body'),
    'kudos_text': fields.String,
    'uri': fields.Url('email_action', absolute=True, scheme='https'),
    'user_id': fields.Integer
    # # @TODO - add user_uri?
    # 'user_uri': field.Url('user', absolute=True)
}

# define resources, routes, and argument validation
class EmailActionListAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, required = True, help = 'A title is required', location = 'json')
        self.reqparse.add_argument('headline', type = str, location = 'json')
        self.reqparse.add_argument('description', type = str, location = 'json')
        self.reqparse.add_argument('list_start_datetime', type = str, location = 'json')
        self.reqparse.add_argument('list_end_datetime', type = str, location = 'json')
        self.reqparse.add_argument('target_email', type = str, location = 'json')
        self.reqparse.add_argument('target_name', type = str, location = 'json')
        self.reqparse.add_argument('target_official_type', type = str, location = 'json')
        self.reqparse.add_argument('email_subject', type = str, location = 'json')
        self.reqparse.add_argument('body', type = str, location = 'json')
        self.reqparse.add_argument('kudos_text', type = str, location = 'json')
        self.reqparse.add_argument('user_id', type = int, location = 'json')

        super(EmailActionListAPI, self).__init__()

    def get(self):
        email_actions_query = EmailAction.query.all()
        return { 'email_actions': [marshal(email_action, email_action_public_fields) for email_action in email_actions_query] }

    def post(self):
        try:
            args = self.reqparse.parse_args()
            new_email_action = EmailAction(
                title = args['title'],
                headline = args['headline'],
                description = args['description'],
                list_start_datetime = args['list_start_datetime'],
                list_end_datetime = args['list_end_datetime'],
                target_email = args['target_email'],
                target_name = args['target_name'],
                target_official_type = args['target_official_type'],
                email_subject = args['email_subject'],
                body = args['body'],
                kudos_text = args['kudos_text'],
                user_id = args['user_id'] # this might need to reference the user instance itself
            )
            new_email_action.add(new_email_action)
            # or could set new_email_action.user(User.query.get(['user_id']))
            return { 'email_action': marshal(new_email_action, email_action_public_fields) }, 201

        except Exception as err:
            db.session.rollback()
            resp = jsonify({"error": str(err)})
            resp.status_code = 403
            return resp

class EmailActionAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, location = 'json')
        self.reqparse.add_argument('headline', type = str, location = 'json')
        self.reqparse.add_argument('description', type = str, location = 'json')
        self.reqparse.add_argument('list_start_datetime', type = str, location = 'json')
        self.reqparse.add_argument('list_end_datetime', type = str, location = 'json')
        self.reqparse.add_argument('target_email', type = str, location = 'json')
        self.reqparse.add_argument('target_name', type = str, location = 'json')
        self.reqparse.add_argument('target_official_type', type = str, location = 'json')
        self.reqparse.add_argument('email_subject', type = str, location = 'json')
        self.reqparse.add_argument('body', type = str, location = 'json')
        self.reqparse.add_argument('kudos_text', type = str, location = 'json')
        self.reqparse.add_argument('user_id', type = int, location = 'json')

        super(EmailActionAPI, self).__init__()

    def get(self, id):
        email_action = EmailAction.query.get_or_404(id)
        return { 'email_action': marshal(email_action, email_action_public_fields) }

    def put(self, id):
        email_action = EmailAction.query.get_or_404(id)
        args = self.reqparse.parse_args()
        for k, v in args.iteritems():
            if v != None:
                setattr(email_action, k, v)
        email_action.update()
        return self.get(id)

    def delete(self, id):
        email_action = EmailAction.query.get_or_404(id)
        email_action.delete(email_action)
        return { 'result': True }
