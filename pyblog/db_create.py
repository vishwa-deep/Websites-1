__author__ = 'admin'
from views import db
from models import Post
from datetime import date


db.create_all()

db.session.add(Post('First post', 'this is my first post', date(2014, 10, 03), None, 1))
db.session.commit()