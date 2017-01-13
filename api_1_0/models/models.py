# imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# App setup
app = Flask(__name__)
app.config.from_pyfile('../../config.py')
db = SQLAlchemy(app)

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

# User model
class User(db.Model, CRUD):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(28), unique=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(30))
    about = db.Column(db.Text)
    zip = db.Column(db.String(5))

    # # @TODO - implement or remove
    # def __init__(self, ..args)

    def __repr__(self):
        return '<User %r>' % self.user_name
