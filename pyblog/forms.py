__author__ = 'admin'

from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired


class AddPost(Form):
    title = StringField('Title', validators=[DataRequired()])
    post_body = TextAreaField('Post', validators=[DataRequired()])


class LoginForm(Form):
    uid = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])