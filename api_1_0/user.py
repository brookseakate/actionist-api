# package imports
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, reqparse, fields, marshal

# relative imports
from models.models import *

# App setup
app = Flask(__name__)
app.config.from_pyfile('../config.py')
db = SQLAlchemy(app)

# public field definitions (for use with marshal)
user_public_fields = {
    'id': fields.Integer,
    'user_name': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'about': fields.String,
    'zip': fields.String,
    'uri': fields.Url('user', absolute=True)
    # @TODO: use below version for https!
    # 'uri': fields.Url('user', absolute=True, scheme='https')
}

# define resources, routes, and argument validation
class UserListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_name', type = str, required = True, help = 'No user name provided', location = 'json')
        self.reqparse.add_argument('first_name', type = str, required = True, help = 'No first name provided', location = 'json')
        self.reqparse.add_argument('last_name', type = str, required = True, help = 'No last name provided', location = 'json')
        self.reqparse.add_argument('zip', type = str, required = True, help = 'No zip code provided', location = 'json')
        self.reqparse.add_argument('about', type = str, default = '', location = 'json')
        super(UserListAPI, self).__init__()

    def get(self):
        users_query = User.query.all()
        return { 'users': [marshal(user, user_public_fields) for user in users_query] }

    def post(self):
        try:
            args = self.reqparse.parse_args()
            new_user = User(
                user_name = args['user_name'],
                first_name = args['first_name'],
                last_name = args['last_name'],
                about = args['about'],
                zip = args['zip']
            )
            new_user.add(new_user)
            return { 'user': marshal(new_user, user_public_fields) }, 201
        # @TODO - fix error handling here (session not rolling back properly. Also clobbering validation errors into generic 400s)
        except Exception as err:
            db.session.rollback()
            resp = jsonify({"error": str(err)})
            resp.status_code = 403
            return resp

class UserAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_name', type = str, location = 'json')
        self.reqparse.add_argument('first_name', type = str, location = 'json')
        self.reqparse.add_argument('last_name', type = str, location = 'json')
        self.reqparse.add_argument('zip', type = str, location = 'json')
        self.reqparse.add_argument('about', type = str, location = 'json')
        super(UserAPI, self).__init__()

    def get(self, id):
        user = User.query.get_or_404(id)
        return { 'user': marshal(user, user_public_fields) }

    def put(self, id):
        # @TODO - add error handling (see POST)
        user = User.query.get_or_404(id)
        args = self.reqparse.parse_args()
        for k, v in args.iteritems():
            if v != None:
                setattr(user, k, v)
        user.update()
        return self.get(id)

    def delete(self, id):
        user = User.query.get_or_404(id)
        user.delete(user)
        return { 'result': True }
