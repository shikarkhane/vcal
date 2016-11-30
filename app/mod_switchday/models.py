# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from app.common.models import Base

# Define a User model
class User(Base):

    __tablename__ = 'user'

    # Identification Data: email & password
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(128),  nullable=False, unique=True)
    password = db.Column(db.String(192),  nullable=True)
    auth_token = db.Column(db.String(300), nullable=True)

    # Authorisation Data: role & status
    role     = db.Column(db.SmallInteger, nullable=False)
    status   = db.Column(db.SmallInteger, nullable=False)

    # New instance instantiation procedure
    def __init__(self, name, email, password, token):

        self.name     = email.split('@')[0]
        self.email    = email
        self.password = password
        self.auth_token = token

    def __repr__(self):
        return '<User %r>' % (self.email)
