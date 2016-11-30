# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from app.common.models import Base

# Define a User model
class Term(Base):

    __tablename__ = 'term'

    # Identification Data: email & password
    group_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    family_spread = db.Column(db.String(300),  nullable=False)

    # New instance instantiation procedure
    def __init__(self, group_id, name, family_spread):
        self.group_id     = group_id
        self.name    = name
        self.family_spread = family_spread

    def __repr__(self):
        return '<term name %r>' % (self.name)
