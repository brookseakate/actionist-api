# package imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# relative imports
from app import db

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

    # columns
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True)
    device_id = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(255), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    about = db.Column(db.Text)
    street_address_1 = db.Column(db.String(100))
    street_address_2 = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(2))
    zip = db.Column(db.String(5))

    # relationships
    call_actions = db.relationship('CallAction', backref='user')
    email_actions = db.relationship('EmailAction', backref='user')
    event_actions = db.relationship('EventAction', backref='user')


    def __repr__(self):
        return '<User %r>' % self.user_name

    # # @TODO - implement or remove __init__'s
    # def __init__(self, ..args)

# CallAction model
class CallAction(db.Model, CRUD):
    __tablename__ = 'call_actions'

    # columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    headline = db.Column(db.String(100))
    description = db.Column(db.Text)
    list_start_datetime = db.Column(db.DateTime)
    list_end_datetime = db.Column(db.DateTime)
    target_phone_number = db.Column(db.String(10))
    target_name = db.Column(db.String(100))
    target_official_type = db.Column(db.String(100))
    script = db.Column(db.Text)
    talking_point_1 = db.Column(db.String(70))
    talking_point_2 = db.Column(db.String(70))
    talking_point_3 = db.Column(db.String(70))
    kudos_text = db.Column(db.String(100))
    # relationship to User who posted this action:
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# EmailAction model
class EmailAction(db.Model, CRUD):
    __tablename__ = 'email_actions'

    # columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    headline = db.Column(db.String(100))
    description = db.Column(db.Text)
    list_start_datetime = db.Column(db.DateTime)
    list_end_datetime = db.Column(db.DateTime)
    target_email = db.Column(db.String(255))
    target_name = db.Column(db.String(100))
    target_official_type = db.Column(db.String(60))
    email_subject = db.Column(db.String(255))
    body = db.Column(db.Text)
    kudos_text = db.Column(db.String(100))
    # relationship to User who posted this action:
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# EventAction model
class EventAction(db.Model, CRUD):
    __tablename__ = 'event_actions'

    # columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    headline = db.Column(db.String(100))
    description = db.Column(db.Text)
    list_start_datetime = db.Column(db.DateTime)
    list_end_datetime = db.Column(db.DateTime)
    location = db.Column(db.String(500))
    event_start_datetime = db.Column(db.DateTime)
    event_end_datetime = db.Column(db.DateTime)
    kudos_text = db.Column(db.String(100))
    # relationship to User who posted this action:
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
