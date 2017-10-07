# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from flywheel import Field, NUMBER, STRING, GlobalIndex
from app.common.models import DyBase

# Define a User model
class EmailNotify(DyBase):

    __tablename__ = 'email_notify'
    __metadata__ = {
        'throughput': {
            'read': 1,
            'write': 1,
        },
        'global_indexes': [
            GlobalIndex.all('ts-index', 'email', 'date_created').throughput(read=1, write=1),
        ],
    }

    # Identification Data: email & password
    email = Field(data_type=STRING, nullable=False)
    type = Field(data_type=STRING, nullable=False)

    # New instance instantiation procedure
    def __init__(self, email, type):
        super(EmailNotify, self).__init__()
        self.email     = email
        self.type = type

    def __repr__(self):
        return '<email %r>' % (self.email)
