import os

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.path.dirname(__file__), 'db.sqlite')

SECURITY_EMAIL_SENDER = "noreply@uppf.in"
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_CHANGEABLE = True

MISAKA_EXTENSIONS = ['tables']
