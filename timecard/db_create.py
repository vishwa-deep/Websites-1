from views import db
from models import TimeEntry, User
from datetime import datetime, date

db.create_all()

mnorman = User(name='mnorman', email='mike@mlnorman.com', temp_pass=None, role='user')
mnorman.hash_password('aaaaaa')
tom = User(name='tom', email='tom@example.com', temp_pass=None, role='user')
tom.hash_password('aaaaaa')
jdoe = User(name='jdoe', email='joe@example.com', temp_pass=None, role='user')
jdoe.hash_password('aaaaaa')
mike = User(name='Mike', email='mike@mlnorman.com', temp_pass=None, role='admin')
mike.hash_password('aaaaaa')
db.session.add(TimeEntry(date.today(), datetime.now(), None, None, None, 0, 1))
db.session.add(mnorman)
db.session.add(jdoe)
db.session.add(tom)
db.session.add(mike)


db.session.commit()