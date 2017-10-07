# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app.common.models import DyBase
from flywheel import Field, NUMBER, GlobalIndex, STRING

# Define a User model

class PublicHoliday(DyBase):

    __tablename__ = 'public_holiday'

    __metadata__ = {
        'throughput': {
            'read': 1,
            'write': 1,
        },

        'global_indexes': [
            GlobalIndex.all('ts-index', 'group_id').throughput(read=1, write=1),
        ],
    }
    created_by_id = Field(data_type=STRING, nullable=False)
    group_id = Field(data_type=STRING, nullable=False)
    holiday_date    = Field(data_type=NUMBER,  nullable=False)
    # full day or half day
    is_halfday   = Field(data_type=NUMBER, nullable=False)

    # New instance instantiation procedure
    def __init__(self, created_by_id, group_id, date, is_halfday):
        super(PublicHoliday, self).__init__()
        self.created_by_id = created_by_id
        self.group_id = group_id
        self.holiday_date  = date
        self.is_halfday    = is_halfday

    def __repr__(self):
        return '<Date %r>' % (str(self.holiday_date))
    def __getitem__(self, key):
        return self.holiday_date
