# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app.common.models import DyBase
from flywheel import Field, NUMBER, STRING

class Term(DyBase):

    __tablename__ = 'term'

    group_id = Field(data_type=NUMBER, nullable=False)
    name = Field(data_type=STRING, nullable=False)
    start_date = Field(data_type=NUMBER, nullable=False)
    end_date = Field(data_type=NUMBER, nullable=False)
    family_spread = Field(data_type=STRING,  nullable=False)

    # New instance instantiation procedure
    def __init__(self, group_id, name, start_dt, end_dt, family_spread):
        self.group_id     = group_id
        self.name    = name
        self.start_date  =start_dt
        self.end_date = end_dt
        self.family_spread = family_spread

    def __repr__(self):
        return '<term name %r>' % (self.name)

class Children(DyBase):

    __tablename__ = 'term_children'

    term_id = Field(data_type=NUMBER, nullable=False)
    child_count = Field(data_type=NUMBER, nullable=False)

    # New instance instantiation procedure
    def __init__(self, term_id, child_count):
        self.term_id     = term_id
        self.child_count    = child_count

    def __repr__(self):
        return '<term id %r>' % (self.term_id)
