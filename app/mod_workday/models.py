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
    created_by_id = db.Column(db.Integer, nullable=False)

    # New instance instantiation procedure
    def __init__(self, created_by_id, group_id, work_date, standin_count, from_time, to_time):
        self.created_by_id = created_by_id
        self.group_id = group_id
        self.work_date = work_date
        self.standin_count = standin_count
        self.from_time_in_24hours = from_time
        self.to_time_in_24hours = to_time

    def __repr__(self):
        return '<Work_date %r>' % (self.work_date)


class Summon(Base):

    __tablename__ = 'summon'

    created_by_id = db.Column(db.Integer, nullable=False)
    group_id = db.Column(db.Integer, nullable=False)
    work_date = db.Column(db.DateTime, nullable=False)
    from_time_in_24hours = db.Column(db.String, default = '0900')
    to_time_in_24hours = db.Column(db.String, default = '1630')

    # New instance instantiation procedure
    def __init__(self, created_by_id, group_id, work_date, from_time, to_time):
        self.created_by_id = created_by_id
        self.group_id = group_id
        self.work_date = work_date
        self.from_time_in_24hours = from_time
        self.to_time_in_24hours = to_time

    def __repr__(self):
        return '<Work_date %r>' % (self.work_date)
