# imports
from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal

# App setup
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
api = Api(app)

# Users array (hard-coded initial data)
users_array = [
    {
        'id': 1,
        'user_name': 'quokka',
        'first_name': 'Quokka',
        'last_name': 'Wokka',
        'about': 'just chillin like a villain',
        'zip': '11206'
    },
    {
        'id': 2,
        'user_name': 'duckie',
        'first_name': 'Duck Duck',
        'last_name': 'Goose',
        'about': '*not* a moose',
        'zip': '97138'
    },
    {
        'id': 3,
        'user_name': 'platypus',
        'first_name': 'Platty',
        'last_name': 'Cake',
        'about': 'pancakes plz?',
        'zip': '02912'
    }
]

# Class to add, update and delete data via SQLAlchemy sessions
class CRUD():
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()

# User model (test)
class User(db.Model, CRUD):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(28), unique=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(30))
    about = db.Column(db.Text)
    zip = db.Column(db.String(5))

    # @TODO - remove, this is redundant with how SQLAlchemy models get built.
    # def __init__(self, args):
    #     # id?
    #     self.user_name = args['user_name']
    #     self.first_name = args['first_name']
    #     self.last_name = args['last_name']
    #     self.about = args['about']
    #     self.zip = args['zip']

    def __repr__(self):
        return '<User %r>' % self.user_name

# public field definitions (for use with marshal)
user_public_fields = {
    'id': fields.Integer,
    'user_name': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'about': fields.String,
    'zip': fields.String,
    'uri': fields.Url('user', absolute=True)
    # 'uri': fields.Url('user', absolute=True, scheme='https') # @TODO: use this for https!
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
        # NOTE: this *works* for getting data from db!
        users_query = User.query.all()
        return { 'users': [marshal(user, user_public_fields) for user in users_query] }

        # users_query = User.query.all()
        # return jsonify({ 'users': users_query })


        # @TODO - remove, this was for hard-coded array of users
        # return { 'users': [marshal(user, user_public_fields) for user in users] }

    def post(self):
        # NOTE: this *works* with db!
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

        # @TODO - remove, this was for hard-coded array of users
        # args = self.reqparse.parse_args()
        # new_user = {
        #     'id': users[-1]['id'] + 1,
        #     'user_name': args['user_name'],
        #     'first_name': args['first_name'],
        #     'last_name': args['last_name'],
        #     'about': args['about'],
        #     'zip': args['zip'],
        # }
        # users.append(new_user)
        # return { 'user': marshal(new_user, user_public_fields) }, 201

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
        # NOTE: this *works* for getting data from db!
        user = User.query.get_or_404(id)
        return { 'user': marshal(user, user_public_fields) }

        # @TODO - remove, this was for hard-coded array of users
        # user = [user for user in users if user['id'] == id]
        # if len(user) == 0:
        #     abort(404)
        # return { 'user': marshal(user[0], user_public_fields) }

    def put(self, id):
        # NOTE: this *works* with db!
        user = User.query.get_or_404(id)
        args = self.reqparse.parse_args()
        for k, v in args.iteritems():
            if v != None:
                setattr(user, k, v)
        user.update()
        return self.get(id)

        # @TODO - remove, this was for hard-coded array of users
        # user = [user for user in users if user['id'] == id]
        # if len(user) == 0:
        #     abort(404)
        # user = user[0]
        # args = self.reqparse.parse_args()
        # for k, v in args.iteritems():
        #     if v != None:
        #         user[k]= v
        # return { 'user': marshal(user, user_public_fields) }

    def delete(self, id):
        # NOTE: this *works* with db!
        user = User.query.get_or_404(id)
        user.delete(user)
        return { 'result': True }

        # # @TODO - remove, this was for hard-coded array of users
        # user = [user for user in users if user['id'] == id]
        # if len(user) == 0:
        #     abort(404)
        # users.remove(user[0])
        # return { 'result': True }

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
