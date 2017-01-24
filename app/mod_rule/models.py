# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from flywheel import Field, NUMBER, STRING
from app.common.models import DyBase

# Define a User model
class Rule(DyBase):

    __tablename__ = 'rule'

    # Identification Data: email & password
    group_id = Field(data_type=NUMBER, nullable=False)
    term_id = Field(data_type=NUMBER, nullable=False)
    definition = Field(data_type=STRING, nullable=False)

    # New instance instantiation procedure
    def __init__(self, group_id, term_id, definition):
        super(Rule, self).__init__()
        self.group_id     = group_id
        self.term_id = term_id
        self.definition    = definition

    def __repr__(self):
        return '<group %r>' % (self.group_id)
