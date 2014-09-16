__author__ = 'admin'

import os


basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = "tasks.db"
SECRET_KEY = "key"


DATABASE_PATH = os.path.join(basedir, DATABASE)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH