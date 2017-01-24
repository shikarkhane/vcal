# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.

from flywheel import Field, NUMBER, STRING
from app.common.models import DyBase

class Invite(DyBase):

    __tablename__ = 'invite'

    email = Field(data_type=STRING, nullable=False)
    group_id = Field(data_type=NUMBER, nullable=False)
    invite_token = Field(data_type=STRING, nullable=True)

    # New instance instantiation procedure
    def __init__(self, email, group_id, invite_token):
        super(Invite, self).__init__()
        self.email = email
        self.group_id = group_id
        self.invite_token = invite_token

    def __repr__(self):
        return '<Email %r>' % (self.email)

class Member(DyBase):

    __tablename__ = 'group_member'

    group_id = Field(data_type=NUMBER, nullable=False)
    user_id = Field(data_type=NUMBER, nullable=False)

    # New instance instantiation procedure
    def __init__(self, group_id, user_id):
        super(Member, self).__init__()
        self.group_id = group_id
        self.user_id = user_id

    def __repr__(self):
        return '<User_id %r>' % (self.user_id)

class User(DyBase):

    __tablename__ = 'user'

    # Identification Data: email & password
    name = Field(data_type=STRING, nullable=False)
    given_name = Field(data_type=STRING, nullable=False)
    family_name = Field(data_type=STRING, nullable=False)
    email = Field(data_type=STRING,  nullable=False)
    password = Field(data_type=STRING,  nullable=True)
    auth_token = Field(data_type=STRING, nullable=True)
    image_url = Field(data_type=STRING, nullable=True)

    # Authorisation Data: role & status
    role     = Field(data_type=NUMBER, nullable=False, default=1)
    is_active   = Field(data_type=NUMBER, nullable=False, default=True)

    # New instance instantiation procedure
    def __init__(self, name, givenName, familyName, email, password, token, imageUrl):
        super(User, self).__init__()
        self.name     = name
        self.given_name = givenName
        self.family_name = familyName
        self.email    = email
        self.password = password
        self.auth_token = token
        self.image_url = imageUrl

    def __repr__(self):
        return '<User %r>' % (self.email)
