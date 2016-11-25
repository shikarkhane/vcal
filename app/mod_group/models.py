# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db


from app.common.models import Base
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
