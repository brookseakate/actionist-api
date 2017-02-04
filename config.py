import os
from os.path import join, dirname
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# add SQLAchemy URI for Postgres.app localhost
SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
SQLALCHEMY_TRACK_MODIFICATIONS = False

HTTP_AUTH_PASSWORD = os.environ['HTTP_AUTH_PASSWORD']

HTTP_AUTH_USERNAME = os.environ['HTTP_AUTH_USERNAME']
