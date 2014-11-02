import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'timecard.db'
SECRET_KEY='test'
WTF_CSRF_ENABLED = True
CSRF_ENABLED = True


#################
# Mail Settings #
#################
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'michaellamarnorman'
MAIL_PASSWORD = 'jtwn=794'

# administrator list
ADMINS = ['michaellamarnorman@gmail.com']


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, DATABASE)