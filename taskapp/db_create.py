__author__ = 'admin'


from views import db

from models import Task

db.create_all()

db.session.add(Task('Create Database', 1))

db.session.add(Task("make portfolio", 1))

db.session.commit()