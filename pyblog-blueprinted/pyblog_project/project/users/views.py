__author__ = 'mike'

# from flask.ext.sqlalchemy import SQLAlchemy
# from sqlalchemy.exc import IntegrityError
# import datetime
# from flask.ext.admin import Admin
# from admin import MyView, AuthenticatedMenuLink, MyModel
# from flask.ext.login import LoginManager, logout_user, login_user, current_user, login_required


from flask import Flask, render_template, request, url_for, flash, redirect, session, Blueprint
from project import db
from project import app

from project.models import User
from forms import LoginForm
from flask.ext.login import login_required, current_user, login_user, logout_user
from project import login_manager
from project.views import flash_errors
#################################
#       Config                  #
#################################

users_blueprint = Blueprint(
        'users', __name__,
        url_prefix='/users',
        template_folder='templates',
        static_folder='static'
    )


# app = Flask(__name__)
# app.config.from_object('config')
#login_manager = LoginManager()
#login_manager.init_app(app)
# db = SQLAlchemy(app)
# admin = Admin(app)
# admin.add_view(MyView(name='Index'))
#login_manager.login_view = 'login'
# from models import Post, User
# admin.add_view(MyModel(Post, db.session))
# admin.add_link(AuthenticatedMenuLink(name='Logout', endpoint='logout'))



@login_manager.user_loader
def load_user(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (username) user to retrieve
    """
    return User.query.get(user_id)



@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    error = None
    if current_user.is_authenticated():
        return redirect('/admin/')
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(user_id=form.uid.data).first()
            if not user or not user.verify_password(form.password.data):
                error = "Username or password does not exist!"
                return render_template('login.html', form=form, error=error)
            else:
                user.authenticated = True
                #session['logged_in'] = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=False)
                return redirect('admin')
        else:
            flash_errors(form)
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('posts.home'))
