# package imports
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, reqparse, fields, marshal

# relative imports
from ..app import db
from ..models import User

# public field definitions (for use with marshal)
user_public_fields = {
    'id': fields.Integer,
    'user_name': fields.String,
    'device_id': fields.String, # @TODO - remove?
    'email': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'about': fields.String,
    'street_address_1': fields.String,
    'street_address_2': fields.String,
    'city': fields.String,
    'state': fields.String,
    'zip': fields.String,
    'uri': fields.Url('user', absolute=True)
    # @TODO: use below version for https!
    # 'uri': fields.Url('user', absolute=True, scheme='https')
}

# define resources, routes, and argument validation
class UserListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_name', type = str, location = 'json')
        self.reqparse.add_argument('device_id', type = str, location = 'json')
        # # @TODO - require device_id argument!
        # self.reqparse.add_argument('device_id', type = str, required = True, help = 'Device ID required', location = 'json')
        self.reqparse.add_argument('email', type = str, location = 'json')
        self.reqparse.add_argument('first_name', type = str, location = 'json')
        self.reqparse.add_argument('last_name', type = str, location = 'json')
        self.reqparse.add_argument('about', type = str, location = 'json')
        self.reqparse.add_argument('street_address_1', type = str, location = 'json')
        self.reqparse.add_argument('street_address_2', type = str, location = 'json')
        self.reqparse.add_argument('city', type = str, location = 'json')
        self.reqparse.add_argument('state', type = str, location = 'json')
        self.reqparse.add_argument('zip', type = str, location = 'json')

        super(UserListAPI, self).__init__()

    def get(self):
        users_query = User.query.all()
        return { 'users': [marshal(user, user_public_fields) for user in users_query] }

    def post(self):
        try:
            args = self.reqparse.parse_args()
            new_user = User(
                user_name = args['user_name'],
                device_id = args['device_id'],
                email = args['email'],
                first_name = args['first_name'],
                last_name = args['last_name'],
                about = args['about'],
                street_address_1 = args['street_address_1'],
                street_address_2 = args['street_address_2'],
                city = args['city'],
                state = args['state'],
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
        self.reqparse.add_argument('device_id', type = str, location = 'json')
        self.reqparse.add_argument('email', type = str, location = 'json')
        self.reqparse.add_argument('first_name', type = str, location = 'json')
        self.reqparse.add_argument('last_name', type = str, location = 'json')
        self.reqparse.add_argument('about', type = str, location = 'json')
        self.reqparse.add_argument('street_address_1', type = str, location = 'json')
        self.reqparse.add_argument('street_address_2', type = str, location = 'json')
        self.reqparse.add_argument('city', type = str, location = 'json')
        self.reqparse.add_argument('state', type = str, location = 'json')
        self.reqparse.add_argument('zip', type = str, location = 'json')

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
