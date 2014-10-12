__author__ = 'admin'
from views import db
from models import Post, User
from datetime import date


db.create_all()

db.session.add(Post('First post', 'this is my first post','Welcome', date(2014, 10, 03), None, 1))
db.session.add(User('admin', 'password', False))

db.session.commit()