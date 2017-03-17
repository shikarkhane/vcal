# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.

from flywheel import Field, NUMBER, STRING
from app.common.models import DyBase

# Define a User model
class Group(DyBase):

    __tablename__ = 'group'

    # Identification Data: email & password
    name = Field(data_type=STRING)
    type_id = Field(data_type=NUMBER)
    default_term_id = Field(data_type=STRING, nullable=True)
    # New instance instantiation procedure
    def __init__(self, name, type_id):
        super(Group, self).__init__()
        self.name     = name
        self.type_id = type_id

    def __repr__(self):
        return '<Group %r>' % (self.name)
