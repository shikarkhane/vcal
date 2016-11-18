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
class Group(Base):

    __tablename__ = 'group'

    # Identification Data: email & password
    name = db.Column(db.String(100), nullable=False)
    type_id = db.Column(db.SmallInteger)
    # New instance instantiation procedure
    def __init__(self, name, type_id):
        self.name     = name
        self.type_id = type_id

    def __repr__(self):
        return '<User %r>' % (self.email)
