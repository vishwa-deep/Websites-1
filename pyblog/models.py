__author__ = 'admin'

from views import db

class Post(db.Model):
    import datetime

    __tablename__ = 'posts'

    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    post_body = db.Column(db.Text, nullable=False)
    posted_date = db.Column(db.Date, default=datetime.datetime.now())
    updated_at = db.Column(db.Date, nullable=True)
    status = db.Column(db.Integer, nullable=False)

    def __init__(self, title, post_body, posted_date, updated_at, status):
        self.title = title
        self.post_body = post_body
        self.posted_date = posted_date
        self.updated_at = updated_at
        self.status = status

    def __repr__(self):
        return '<title %r>' % self.title