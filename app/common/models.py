# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
import time

from flywheel import Model, Field, NUMBER

class DyBase(Model):

    __abstract__  = True

    id            = Field(data_type=NUMBER)
    date_created  = Field(NUMBER,  default=int(time.time()))
    date_modified = Field(NUMBER,  default=int(time.time()))
