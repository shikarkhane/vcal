# Import the database object (db) from the main application module
# We will define this inside /base/__init__.py in the next sections.
import time
import uuid

from flywheel import Model, Field, NUMBER, STRING

class DyBase(Model):

    __abstract__  = True

    id            = Field(data_type=STRING, hash_key=True)
    date_created  = Field(data_type=NUMBER)
    date_modified = Field(data_type=NUMBER)

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.date_created = int(time.time())
        self.date_modified = int(time.time())
