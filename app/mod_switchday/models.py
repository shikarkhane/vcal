# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from app.common.models import Base

class Switchday(Base):

    __tablename__ = 'switchday'

    group_id = db.Column(db.Integer, nullable=False)
    switch_date = db.Column(db.DateTime, nullable=False)
    from_time_in_24hours = db.Column(db.String, default = '0900')
    to_time_in_24hours = db.Column(db.String, default = '1630')
    standin_user_id = db.Column(db.Integer, nullable=True)
    is_half_day = db.Column(db.Boolean, nullable=False, default=False)
    is_work_day = db.Column(db.Boolean, nullable=False, default=False)

    # New instance instantiation procedure
    def __init__(self, group_id, switch_date, from_time, to_time,
                 standin_user_id, is_half_day, is_work_day):
        self.group_id = group_id
        self.switch_date = switch_date
        self.from_time_in_24hours = from_time
        self.to_time_in_24hours = to_time
        self.standin_user_id = standin_user_id
        self.is_half_day = is_half_day
        self.is_work_day = is_work_day

    def __repr__(self):
        return '<Switch_date %r>' % (self.switch_date)