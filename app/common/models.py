# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
import time

from flywheel import Model, Field, NUMBER

class DyBase(Model):

    __abstract__  = True

    id            = Field(data_type=NUMBER, hash_key=True)
    date_created  = Field(data_type=NUMBER)
    date_modified = Field(data_type=NUMBER)

    def __init__(self):
        self.id = int(time.time())
        self.date_created = int(time.time())
        self.date_modified = int(time.time())
