__author__ = 'admin'

from views import db


class Post(db.Model):
    import datetime

    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    post_body = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String, nullable=False)
    posted_date = db.Column(db.Date, default=datetime.datetime.utcnow())
    updated_at = db.Column(db.Date, nullable=True)
    status = db.Column(db.Integer, default=1)

    def __init__(self, title='', post_body='', tags='', posted_date=datetime.datetime.utcnow(), updated_at=None, status=1):
        self.title = title
        self.post_body = post_body
        self.tags = tags
        self.posted_date = posted_date
        self.updated_at = updated_at
        self.status = status

    def __repr__(self):
        return '<title %r>' % self.title


class User(db.Model):

    __tablename__ = 'users'


    user_id = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, user_id, password, authenticated):
        self.user_id = user_id
        self.password = password
        self.authenticated= authenticated

    def __repr__(self):
        return '<User %r>' % self.user_id

    def is_active(self):
        return True

    def get_id(self):
        return self.user_id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False