# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from app.common.models import Base

# Define a User model

class PublicHoliday(Base):

    __tablename__ = 'public_holiday'

    # date
    holiday_date    = db.Column(db.DateTime,  nullable=False)
    # full day or half day
    is_halfday   = db.Column(db.SmallInteger, nullable=False)

    # New instance instantiation procedure
    def __init__(self, date, is_halfday):

        self.holiday_date  = date
        self.is_halfday    = is_halfday

    def __repr__(self):
        return '<Date %r>' % (str(self.holiday_date))
