# Import the database object (db) from the main application module
# We will define this inside /base/__init__.py in the next sections.

from flywheel import Field, NUMBER, STRING, GlobalIndex
from base.common.models import DyBase

# Define a User model
class Group(DyBase):

    __tablename__ = 'group'
    __metadata__ = {
        'throughput': {
            'read': 1,
            'write': 1,
        },

        'global_indexes': [
            GlobalIndex.all('ts-index', 'domain').throughput(read=1, write=1),
        ],

    }
    # Identification Data: email & password
    name = Field(data_type=STRING)
    type_id = Field(data_type=NUMBER)
    domain = Field(data_type=STRING)
    default_term_id = Field(data_type=STRING, nullable=True)
    # New instance instantiation procedure
    def __init__(self, name, type_id, domain):
        super(Group, self).__init__()
        self.name     = name
        self.type_id = type_id
        self.domain = domain

    def __repr__(self):
        return '<Group %r>' % (self.name)
    def __getitem__(self, key):
        return self.id