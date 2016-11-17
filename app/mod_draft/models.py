# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

# Define a User model
class User(Base):

    __tablename__ = 'user'

    # Identification Data: email & password
    email    = db.Column(db.String(128),  nullable=False,
                                            unique=True)
    password = db.Column(db.String(192),  nullable=True)
    auth_token = db.Column(db.String(300), nullable=True)

    # Authorisation Data: role & status
    role     = db.Column(db.SmallInteger, nullable=False)
    status   = db.Column(db.SmallInteger, nullable=False)

    # New instance instantiation procedure
    def __init__(self, name, email, password, token):

        self.name     = name
        self.email    = email
        self.password = password
        self.auth_token = token

    def __repr__(self):
        return '<User %r>' % (self.name)

class PublicHoliday(Base):

    __tablename__ = 'public_holiday'

    # date
    holiday_date    = db.Column(db.DateTime,  nullable=False)
    # full day or half day
    is_halfday   = db.Column(db.SmallInteger, nullable=False)

    # New instance instantiation procedure
    def __init__(self, date, is_halfday):

        self.holiday_date  = date
        self.is_halfday    = is_halfday

    def __repr__(self):
        return '<Date %r>' % (str(self.holiday_date))