__author__ = 'admin'

from views import db
from passlib.apps import custom_app_context as pwd_context


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
    user_id = db.Column(db.String, db.ForeignKey('users.user_id'))

    def __init__(self, title='', post_body='', tags='', posted_date=datetime.datetime.utcnow(), updated_at=None, status=1, user_id=''):
        self.title = title
        self.post_body = post_body
        self.tags = tags
        self.posted_date = posted_date
        self.updated_at = updated_at
        self.status = status
        self.user_id = user_id

    def __repr__(self):
        return '<title %r>' % self.title


class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.String, primary_key=True)
    password_hash = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)
    post = db.relationship('Post', backref='poster')

    def __init__(self, user_id, authenticated):
        self.user_id = user_id
        self.authenticated = authenticated

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

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