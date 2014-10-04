__author__ = 'mike'

import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'blog.db'

DATABASE_PATH = os.path.join(basedir, DATABASE)

#SQLACHECMY database uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
