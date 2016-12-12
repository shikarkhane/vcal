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
    creator_user_id = db.Column(db.Integer, nullable=False)

    # New instance instantiation procedure
    def __init__(self, creator_user_id, group_id, work_date, standin_count, from_time, to_time):
        self.creator_user_id = creator_user_id
        self.group_id = group_id
        self.work_date = work_date
        self.standin_count = standin_count
        self.from_time_in_24hours = from_time
        self.to_time_in_24hours = to_time

    def __repr__(self):
        return '<Work_date %r>' % (self.work_date)

class StandinDay(Base):

    __tablename__ = 'standinday'

    group_id = db.Column(db.Integer, nullable=False)
    standin_date = db.Column(db.DateTime, nullable=False)
    standin_user_id = db.Column(db.Integer, nullable=True)
    booking_date = db.Column(db.DateTime, nullable=False)

    # New instance instantiation procedure
    def __init__(self, group_id, standin_date, standin_user_id, booking_date):
        self.group_id = group_id
        self.standin_date = standin_date
        self.standin_user_id = standin_user_id
        self.booking_date = booking_date

    def __repr__(self):
        return '<standin_date %r>' % (self.standin_date)


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
