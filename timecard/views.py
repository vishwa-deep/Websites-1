from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from forms import SelectUser, AdminSearch, LoginForm, ResetPassword
from datetime import date, datetime, timedelta
from functools import wraps
from flask.ext.mail import Mail, Message
from config import ADMINS
import random
import string


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
mail = Mail(app)
from models import User, TimeEntry

def login_required(test):
  @wraps(test)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return test(*args, **kwargs)
    else:
      flash("You must login to access admin!")
      return redirect(url_for('login'))
  return wrap


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text, error), 'error')

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))


def send_message(msg_body, email_recip):
  msg = Message('Password reset', sender=ADMINS[0], recipients=email_recip)
  msg.body = 'Test message'
  msg.html = '''<h2>Your temp password id %s</h2><br><h3> Visit <a href="http://127.0.0.1:5000/reset_password">
  http://127.0.0.1:5000/reset_password</a> to reset it.</h3>''' % msg_body
  with app.app_context():
    mail.send(msg)


def determine_shift(shift, in_or_out):
  dayshift_clockin = False
  dayshift_clockout = False
  lunch_clockout = False
  lunch_clockin = False
  nightshift_clockin = False
  nightshift_clockout = False
  if shift == 'day_shift' and in_or_out == 'clock_in':
    dayshift_clockin = True
  if shift == 'day_shift' and in_or_out == 'clock_out':
    dayshift_clockout = True
  if shift == 'night_shift' and in_or_out == 'clock_in':
    nightshift_clockin = True
  if shift == 'night_shift' and in_or_out == 'clock_out':
    nightshift_clockout = True
  if in_or_out == 'lunch_clock_out':
    lunch_clockout = True
  if in_or_out == 'lunch_clock_in':
    lunch_clockin = True
  return dayshift_clockin, dayshift_clockout, nightshift_clockin, nightshift_clockout, lunch_clockout, lunch_clockin


def dayshift_clockin_func(user_id):
  prev_entry = db.session.query(TimeEntry).filter_by(user_id=user_id, cal_date=date.today()).first()
  error = ""
  if prev_entry:
    error = "You can't clock in twice in one day"
    return error
  time_entry = TimeEntry(
      date.today(),
      datetime.now(),
      None,
      None,   
      None,
      0,
      user_id
     )
  db.session.add(time_entry)
  db.session.commit()
  success = "Added Successfully."
  return success

def dayshift_clockout_func(user_id):
  prev_entry = db.session.query(TimeEntry).filter_by(user_id=user_id, cal_date=date.today()).first()
  error = ""
  if prev_entry and prev_entry.clock_in is not None and prev_entry.clock_out is None:
    prev_entry.clock_out = datetime.now()

    #db.session.add(time_entry)
    db.session.commit()
    success = "Added Successfully."
    return success
  else:
    error = "Never clocked in?  Leave a note."
    return error


def nightshift_clockin_func(user_id):
  prev_entry = db.session.query(TimeEntry).filter_by(user_id=user_id, cal_date=date.today()).first()
  error = ""
  if prev_entry:
    error = "You can't clock in twice in one day"
    return error
  time_entry = TimeEntry(
      date.today(),
      datetime.now(),
      None,
      None,
      None,
      1,
      user_id
     )
  db.session.add(time_entry)
  db.session.commit()
  success = "Added Successfully."
  return success


def nightshift_clockout_func(user_id):
  prev_entry = db.session.query(TimeEntry).filter_by(user_id=user_id, cal_date=date.today()).first()
  error = ""
  if prev_entry and prev_entry.clock_in is not None and prev_entry.clock_out is None:
    prev_entry.clock_out = datetime.now()

    #db.session.add(time_entry)
    db.session.commit()
    success = "Added Successfully."
    return success
  else:
    error = "Never clocked in?  Leave a note."
    return error


def lunch_clockout_func(user_id):
  prev_entry = db.session.query(TimeEntry).filter_by(user_id=user_id, cal_date=date.today()).first()
  error = ""
  if prev_entry and prev_entry.lunch_out is None:
    prev_entry.lunch_out = datetime.now()

    #db.session.add(time_entry)
    db.session.commit()
    success = "Added Successfully."
    return success
  else:
    error = "Never clocked in?  Leave a note."
    return error

def lunch_clockin_func(user_id):
  prev_entry = db.session.query(TimeEntry).filter_by(user_id=user_id, cal_date=date.today()).first()
  error = ""
  if prev_entry and prev_entry.lunch_out and prev_entry.lunch_in is None:
    prev_entry.lunch_in = datetime.now()

    #db.session.add(time_entry)
    db.session.commit()
    success = "Added Successfully."
    return success
  else:
    error = "Never clocked in?  Leave a note."
    return error




@app.route('/', methods=["GET", "POST"])
def index():
  form = SelectUser(request.form)
  form.user.choices = [(u.id, u.name) for u in db.session.query(User).filter_by(role='user').order_by(User.name.asc())]
  if request.method == "POST":
    if form.validate_on_submit():
      shift = form.shift.data
      in_or_out = form.clock_in_out.data
      u = db.session.query(User).filter_by(id=form.user.data).first()
      if u is None or not u.verify_password(form.password.data):
        flash('Username or password is incorrect.')
        return redirect(url_for('index'))
      dayshift_clockin, dayshift_clockout, nightshift_clockin, nightshift_clockout, lunch_clockout, lunch_clockin = determine_shift(shift, in_or_out)


      if dayshift_clockin:
        added = dayshift_clockin_func(form.user.data)
      #k = db.session.query(User).filter_by(id=j).first().name
        flash(added)
      elif dayshift_clockout:
        added = dayshift_clockout_func(form.user.data)
        flash(added)
      elif nightshift_clockin:
        added = nightshift_clockin_func(form.user.data)
        flash (added)
      elif nightshift_clockout:
        added = nightshift_clockout_func(form.user.data)
        flash(added)
      elif lunch_clockout:
        added = lunch_clockout_func(form.user.data)
        flash(added)
      elif lunch_clockin:
        added = lunch_clockin_func(form.user.data)
        flash(added)
    else:
      flash_errors(form)
      return redirect(url_for('index'))
    

  return render_template('index.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm(request.form)
  if 'logged_in' in session:
    return redirect(url_for('admin'))
  if request.method == 'POST':
    if form.validate_on_submit():
      u = db.session.query(User).filter_by(name=form.username.data, role='admin').first()
      if not u or not u.verify_password(form.password.data):
        flash('Username or password is incorrect or you are not an admin.')
        flash_errors(form)
        return render_template('login.html', form=form)
      else:
        session['logged_in'] = True
        #flash('logged in successfully')
        return redirect(url_for('admin'))
  return render_template('login.html', form=form)


@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  return redirect(url_for('index'))


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
  form = ResetPassword(request.form)
  if request.method == 'POST':
    if form.validate_on_submit():
      u = User.query.filter_by(name=form.username.data, temp_pass=form.temp_pass.data).first()
      if u is None:
        flash("Username or passwords incorrect.")
        return render_template('reset_password.html', form=form)
      else:
        u.temp_pass = None
        u.hash_password(form.password.data)
        db.session.commit()
        flash("Password has been reset.")
        return redirect(url_for('index'))
    flash_errors(form)
    return render_template('reset_password.html', form=form)        
  return render_template('reset_password.html', form=form)


@app.route('/admin_view', methods=["GET", "POST"])
@login_required
def admin():
  form = AdminSearch(request.form)
  form.user.choices = [(u.id, u.name) for u in db.session.query(User).filter_by(role='user').order_by(User.name.asc())]
  entries = db.session.query(TimeEntry).order_by(TimeEntry.user_id.asc())
  if request.method == "POST":
    if form.validate_on_submit():
      entries = db.session.query(TimeEntry).filter_by(user_id=form.user.data).order_by(TimeEntry.cal_date.asc())
      return render_template('result.html', entries=entries)
    else:
      flash_errors(form)
      return render_template('success.html', form=form, entries=entries)
  return render_template('success.html', form=form, entries=entries)


@app.route('/send_temp_pass/', methods=['GET', 'POST'])
def send_temp_pass():
  if request.method == 'POST':
    json_results = []
    user_email = request.form.get('email')
    if '@' in user_email:
      rand_pass = id_generator()
      u = db.session.query(User).filter_by(email=user_email).first()
      if u is None:
        data = {
          'success_message': 'Please enter a vaild email.'
        }
        json_results.append(data)
        return jsonify(res=json_results)

      u.temp_pass = rand_pass
      db.session.commit()
      send_message(rand_pass, [user_email])
      val_res = 'Temp password sent to ' + user_email
      data = {
        'success_message': val_res
      }
      json_results.append(data)
      return jsonify(res=json_results)
    

