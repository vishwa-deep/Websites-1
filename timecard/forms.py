from flask_wtf import Form 
from wtforms import SelectField, RadioField, PasswordField, StringField
from wtforms.validators import DataRequired, Length, EqualTo


class SelectUser(Form):
  user = SelectField('Username', coerce=int)
  password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=18)])
  shift = RadioField('Shift', choices=[('day_shift', 'Day Shift'), ('night_shift', 'Night Shift')], validators=[DataRequired()])
  clock_in_out = RadioField('Clock In or Out', choices=[('clock_in', 'Clock In'), ('lunch_clock_out', 'Lunch Clock Out'),
    ('lunch_clock_in', 'Lunch Clock In'), ('clock_out', 'Clock Out')], validators=[DataRequired()])


class AdminSearch(Form):
  user = SelectField('Username', coerce=int)


class LoginForm(Form):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=18)])
  

class ResetPassword(Form):
  username = StringField("Username", validators=[DataRequired()])
  temp_pass = PasswordField("Temp Password", validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=18)])
  confirm = PasswordField('Confirm', validators=[DataRequired(), EqualTo('password', message='Passwords must match' )])