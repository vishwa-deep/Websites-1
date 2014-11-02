from views import db
from passlib.apps import custom_app_context as pwd_context

class TimeEntry(db.Model):
  __tablename__ = 'entries'

  entry_id = db.Column(db.Integer, primary_key=True)
  cal_date = db.Column(db.Date, nullable=False)
  clock_in = db.Column(db.DateTime)
  lunch_out = db.Column(db.DateTime)
  lunch_in = db.Column(db.DateTime)
  clock_out = db.Column(db.DateTime)
  shift = db.Column(db.Integer, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

  def __init__(self, cal_date, clock_in, lunch_out, lunch_in, clock_out, shift, user_id):
    self.cal_date = cal_date
    self.clock_in = clock_in
    self.clock_out = clock_out
    self.shift = shift
    self.user_id = user_id

  def __repr__(self):
    return '<clocked in: %r>' % self.clock_in


class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  email = db.Column(db.String, nullable=False)
  password = db.Column(db.String, nullable=False)
  temp_pass = db.Column(db.String)
  role = db.Column(db.String, nullable=False)
  tasks = db.relationship('TimeEntry', backref='employee')


  def __init__(self, name=None, email=None, password=None, temp_pass=None, role=None):
    self.name = name
    self.email = email
    self.password = password
    self.temp_pass = temp_pass
    self.role = role

  def hash_password(self, password):
    self.password = pwd_context.encrypt(password)

  def verify_password(self, password):
    return pwd_context.verify(password, self.password)

  def __repr__(self):
    return '<name: %r>' % self.name
