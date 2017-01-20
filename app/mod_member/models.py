# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from app.common.models import Base

class Invite(Base):

    __tablename__ = 'invite'

    email = db.Column(db.String(128), nullable=False)
    group_id = db.Column(db.Integer, nullable=False)
    invite_token = db.Column(db.String, nullable=True)

    # New instance instantiation procedure
    def __init__(self, email, group_id, invite_token):
        self.email = email
        self.group_id = group_id
        self.invite_token = invite_token

    def __repr__(self):
        return '<Email %r>' % (self.email)

class Member(Base):

    __tablename__ = 'group_member'

    group_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    # New instance instantiation procedure
    def __init__(self, group_id, user_id):
        self.group_id = group_id
        self.user_id = user_id

    def __repr__(self):
        return '<User_id %r>' % (self.user_id)

class User(Base):

    __tablename__ = 'user'

    # Identification Data: email & password
    name = db.Column(db.String(200), nullable=False)
    given_name = db.Column(db.String(100), nullable=False)
    family_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(128),  nullable=False, unique=True)
    password = db.Column(db.String(192),  nullable=True)
    auth_token = db.Column(db.String(300), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)

    # Authorisation Data: role & status
    role     = db.Column(db.SmallInteger, nullable=False, default=1)
    is_active   = db.Column(db.SmallInteger, nullable=False, default=True)

    # New instance instantiation procedure
    def __init__(self, name, givenName, familyName, email, password, token, imageUrl):

        self.name     = name
        self.given_name = givenName
        self.family_name = familyName
        self.email    = email
        self.password = password
        self.auth_token = token
        self.image_url = imageUrl

    def __repr__(self):
        return '<User %r>' % (self.email)
