# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.

from flywheel import Field, NUMBER, STRING, GlobalIndex
from app.common.models import DyBase

class Workday(DyBase):

    __tablename__ = 'workday'
    __metadata__ = {
        'global_indexes': [
            GlobalIndex.all('ts1-index', 'group_id').throughput(read=1, write=1),
        ],
    }
    group_id = Field(data_type=STRING, nullable=False)
    work_date = Field(data_type=NUMBER, nullable=False)
    from_time_in_24hours = Field(data_type=STRING, default = '0900')
    to_time_in_24hours = Field(data_type=STRING, default = '1630')
    creator_user_id = Field(data_type=STRING, nullable=False)
    standin_user_id = Field(data_type=STRING, nullable=True)
    booking_date = Field(data_type=NUMBER, nullable=False)
    is_half_day = Field(data_type=NUMBER, nullable=False, default=False)
    has_not_worked = Field(data_type=NUMBER, nullable=False, default=False)

    # New instance instantiation procedure
    def __init__(self, creator_user_id, group_id, work_date, from_time, to_time,
                 standin_user_id, booking_date, is_half_day):
        super(Workday, self).__init__()
        self.creator_user_id = creator_user_id
        self.group_id = group_id
        self.work_date = work_date
        self.from_time_in_24hours = from_time
        self.to_time_in_24hours = to_time
        self.standin_user_id = standin_user_id
        self.booking_date = booking_date
        self.is_half_day = is_half_day

    def __repr__(self):
        return '<Work_date %r>' % (self.work_date)
    def __getitem__(self, key):
        return self.work_date
class StandinDay(DyBase):

    __tablename__ = 'standinday'
    __metadata__ = {
        'global_indexes': [
            GlobalIndex.all('ts1-index', 'group_id').throughput(read=1, write=1),
        ],
    }
    group_id = Field(data_type=STRING, nullable=False)
    standin_date = Field(data_type=NUMBER, nullable=False)
    standin_user_id = Field(data_type=STRING, nullable=True)
    booking_date = Field(data_type=NUMBER, nullable=False)
    has_not_worked = Field(data_type=NUMBER, nullable=False, default=False)

    # New instance instantiation procedure
    def __init__(self, group_id, standin_date, standin_user_id, booking_date):
        super(StandinDay, self).__init__()
        self.group_id = group_id
        self.standin_date = standin_date
        self.standin_user_id = standin_user_id
        self.booking_date = booking_date

    def __repr__(self):
        return '<standin_date %r>' % (self.standin_date)

    def __getitem__(self, key):
        return self.standin_date


class Summon(DyBase):

    __tablename__ = 'summon'
    __metadata__ = {
        'global_indexes': [
            GlobalIndex.all('ts-index', 'group_id').throughput(read=1, write=1),
        ],
    }
    created_by_id = Field(data_type=STRING, nullable=False)
    group_id = Field(data_type=STRING, nullable=False)
    work_date = Field(data_type=NUMBER, nullable=False)
    from_time_in_24hours = Field(data_type=STRING, default = '0900')
    to_time_in_24hours = Field(data_type=STRING, default = '1630')

    # New instance instantiation procedure
    def __init__(self, created_by_id, group_id, work_date, from_time, to_time):
        super(Summon, self).__init__()
        self.created_by_id = created_by_id
        self.group_id = group_id
        self.work_date = work_date
        self.from_time_in_24hours = from_time
        self.to_time_in_24hours = to_time

    def __repr__(self):
        return '<Work_date %r>' % (self.work_date)
    def __getitem__(self, key):
        return self.work_date
