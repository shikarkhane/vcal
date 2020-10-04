# Import the database object (db) from the main application module
# We will define this inside /base/__init__.py in the next sections.

from flywheel import Field, NUMBER, STRING, GlobalIndex
from base.common.models import DyBase

class Invite(DyBase):

    __tablename__ = 'invite'
    __metadata__ = {
        'throughput': {
            'read': 1,
            'write': 1,
        },

        'global_indexes': [
            GlobalIndex.all('ts-index', 'group_id').throughput(read=1, write=1),
        ],
    }

    email = Field(data_type=STRING, nullable=False)
    group_id = Field(data_type=STRING, nullable=False)
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
    __metadata__ = {
        'throughput': {
            'read': 1,
            'write': 1,
        },

        'global_indexes': [
            GlobalIndex.all('ts-index1', 'email').throughput(read=1, write=1),
            GlobalIndex.all('ts-index', 'role').throughput(read=1, write=1),
        ],
    }

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
    def __getitem__(self, key):
        return self.email
