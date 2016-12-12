# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from app.common.models import Base


class Term(Base):

    __tablename__ = 'term'

    group_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    family_spread = db.Column(db.String,  nullable=False)

    # New instance instantiation procedure
    def __init__(self, group_id, name, start_dt, end_dt, family_spread):
        self.group_id     = group_id
        self.name    = name
        self.start_date  =start_dt
        self.end_date = end_dt
        self.family_spread = family_spread

    def __repr__(self):
        return '<term name %r>' % (self.name)

class Children(Base):

    __tablename__ = 'term_children'

    term_id = db.Column(db.Integer, nullable=False, unique=True)
    child_count = db.Column(db.Integer, nullable=False)

    # New instance instantiation procedure
    def __init__(self, term_id, child_count):
        self.term_id     = term_id
        self.child_count    = child_count

    def __repr__(self):
        return '<term id %r>' % (self.term_id)
