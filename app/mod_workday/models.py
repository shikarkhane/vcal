# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from app.common.models import Base

class Workday(Base):

    __tablename__ = 'workday'

    group_id = db.Column(db.Integer, nullable=False)
    work_date = db.Column(db.DateTime, nullable=False)
    standin_count = db.Column(db.SmallInteger, nullable=False)
    from_time_in_24hours = db.Column(db.String, default = '0900')
    to_time_in_24hours = db.Column(db.String, default = '1630')

    # New instance instantiation procedure
    def __init__(self, group_id, work_date, standin_count, from_time, to_time):
        self.group_id = group_id
        self.work_date = work_date
        self.standin_count = standin_count
        self.from_time_in_24hours = from_time
        self.to_time_in_24hours = to_time

    def __repr__(self):
        return '<Work_date %r>' % (self.work_date)
