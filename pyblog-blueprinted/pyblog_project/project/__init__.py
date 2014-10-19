from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy 
from flask.ext.admin import Admin
from flask.ext.login import LoginManager
from admin import MyView, MyModel, AuthenticatedMenuLink

app = Flask(__name__)
app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
admin = Admin(app)
admin.add_view(MyView(name='Index'))
login_manager.login_view = 'users.login'
from models import Post, User
admin.add_view(MyModel(Post, db.session))
admin.add_link(AuthenticatedMenuLink(name='Logout', endpoint='users.logout'))



from project.users.views import users_blueprint
from project.posts.views import posts_blueprint

#register blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(posts_blueprint)