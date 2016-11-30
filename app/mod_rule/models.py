# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from app.common.models import Base

# Define a User model
class Rule(Base):

    __tablename__ = 'rule'

    # Identification Data: email & password
    group_id = db.Column(db.Integer, nullable=False, unique=True)
    definition = db.Column(db.String, nullable=False)

    # New instance instantiation procedure
    def __init__(self, group_id, definition):
        self.group_id     = group_id
        self.definition    = definition

    def __repr__(self):
        return '<group %r>' % (self.group_id)
