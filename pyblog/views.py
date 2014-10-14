__author__ = 'mike'

from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from forms import AddPost, LoginForm
import datetime
from flask.ext.admin import Admin
from admin import MyView, AuthenticatedMenuLink, MyModel
from flask.ext.login import LoginManager, logout_user, login_user, current_user, login_required


app = Flask(__name__)
app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
admin = Admin(app)
admin.add_view(MyView(name='Index'))
login_manager.login_view = 'login'
from models import Post, User
admin.add_view(MyModel(Post, db.session))
admin.add_link(AuthenticatedMenuLink(name='Logout', endpoint='logout'))



@login_manager.user_loader
def load_user(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (username) user to retrieve
    """
    return User.query.get(user_id)


@app.route('/')
def home():
    posts = db.session.query(Post).filter_by(status='1').order_by(Post.posted_date.desc())
    return render_template('blog.html', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if current_user.is_authenticated():
        return redirect('/admin/')
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(user_id=form.uid.data).first()
            if not user or not user.verify_password(form.password.data):
                return render_template('login.html', form=form)
            else:
                user.authenticated = True
                #session['logged_in'] = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=False)
                return redirect('admin')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('home'))


# @app.route('/add_post', methods=['GET', 'POST'])
# @login_required
# def add_post():
#     form = AddPost(request.form)
#     if request.method == 'POST':
#         post = Post(
#             form.title.data,
#             form.post_body.data,
#             datetime.utcnow(),
#             None,
#             1
#         )
#         db.session.add(post)
#         db.session.commit()
#         return redirect(url_for('home'))
#     return redirect('/admin')


@app.route('/post/<int:post_id>')
def post(post_id):
    new_id = post_id
    tag = []
    post = db.session.query(Post).filter_by(post_id=new_id)
    for p in post:
        tag = p.tags.split()
    dt = datetime.date.today()

    return render_template('post.html', post=post, tag=tag, dt=dt)
