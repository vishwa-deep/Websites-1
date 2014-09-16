__author__ = 'admin'

import os


basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = "tasks.db"


DATABASE_PATH = os.path.join(basedir, DATABASE)

SQLACHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH