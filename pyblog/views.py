__author__ = 'mike'

from flask import Flask, render_template, request, url_for, flash
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from functools import wraps

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from models import Post

@app.route('/home')
def index():
    return render_template('home.html')


@app.route('/')
def home():
    posts = db.session.query(Post).filter_by(status='1').order_by(Post.posted_date.desc())
    return render_template('blog.html', posts=posts)

