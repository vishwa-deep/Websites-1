__author__ = 'admin'

from views import db


class Task(db.Model):

    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer)

    def __init__(self, task, status):
        self.task = task
        self.status = status

    def __repr__(self):
        return '<name %r>', self.body
