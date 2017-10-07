# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from flywheel import Field, NUMBER, STRING, GlobalIndex
from app.common.models import DyBase


class Switchday(DyBase):

    __tablename__ = 'switchday'
    __metadata__ = {
        'throughput': {
            'read': 1,
            'write': 1,
        },

        'global_indexes': [
            GlobalIndex.all('ts-index', 'group_id').throughput(read=1, write=1),
        ],
    }

    group_id = Field(data_type=STRING, nullable=False)
    switch_date = Field(data_type=NUMBER, nullable=False)
    from_time_in_24hours = Field(data_type=STRING, default = '0900')
    to_time_in_24hours = Field(data_type=STRING, default = '1630')
    standin_user_id = Field(data_type=STRING, nullable=True)
    is_half_day = Field(data_type=NUMBER, nullable=False, default=False)
    is_work_day = Field(data_type=NUMBER, nullable=False, default=False)

    # New instance instantiation procedure
    def __init__(self, group_id, switch_date, from_time, to_time,
                 standin_user_id, is_half_day, is_work_day):
        super(Switchday, self).__init__()
        self.group_id = group_id
        self.switch_date = switch_date
        self.from_time_in_24hours = from_time
        self.to_time_in_24hours = to_time
        self.standin_user_id = standin_user_id
        self.is_half_day = is_half_day
        self.is_work_day = is_work_day

    def __repr__(self):
        return '<Switch_date %r>' % (self.switch_date)
    def __getitem__(self, key):
        return self.switch_date