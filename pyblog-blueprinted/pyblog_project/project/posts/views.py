__author__ = 'mike'

# from flask.ext.sqlalchemy import SQLAlchemy
# from sqlalchemy.exc import IntegrityError
# from forms import AddPost, LoginForm
# from flask.ext.admin import Admin
# from admin import MyView, AuthenticatedMenuLink, MyModel
# from flask.ext.login import LoginManager, logout_user, login_user, current_user, login_required


from flask import Flask, render_template, request, url_for, flash, redirect, session, Blueprint
from project import db
import datetime
from project.models import Post, User



posts_blueprint = Blueprint(
        'posts', __name__,
        url_prefix='/posts',
        template_folder='templates',
        static_folder='static'
    )



# app = Flask(__name__)
# app.config.from_object('config')
# login_manager = LoginManager()
# login_manager.init_app(app)
# db = SQLAlchemy(app)
# admin = Admin(app)
# admin.add_view(MyView(name='Index'))
# login_manager.login_view = 'login'
# from models import Post, User
# admin.add_view(MyModel(Post, db.session))
# admin.add_link(AuthenticatedMenuLink(name='Logout', endpoint='logout'))


@posts_blueprint.route('/')
def home():
    posts = db.session.query(Post).filter_by(status='1').order_by(Post.posted_date.desc())
    return render_template('blog.html', posts=posts)




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


@posts_blueprint.route('/post/<string:post_id>')
def post(post_id):
    new_id = post_id.replace('_', ' ')
    tag = []
    post = db.session.query(Post).filter_by(title=new_id)

    for p in post:
        tag = p.tags.split()
    dt = datetime.date.today()

    return render_template('post.html', post=post, tag=tag, dt=dt)
