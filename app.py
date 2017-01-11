from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

users = [
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

class UserListAPI(Resource):
    def get(self):
        return { 'users': users }

    def post(self):
        pass

class UserAPI(Resource):
    def get(self, id):
        pass

    def post(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass

api.add_resource(UserListAPI, '/api/v1.0/users', endpoint = 'users')
api.add_resource(UserAPI, '/api/v1.0/users/<int:id>', endpoint = 'user')

# NOTE: do not remove!
if __name__ == '__main__':
    app.run(debug=True)
