from base import engine
from base.mod_member.models import User
from base.common.master_data import E_ROLE

# todo: user-group mapping is pending, this method should get by groupId, role.groupadmin
def getGroupAdmins(group_id):
    return engine.query(User).filter(User.role == E_ROLE.GroupAdmin).all()

def getAllUsers(group_id):
    return engine.scan(User).all(attributes=['id', 'name', 'given_name', 'family_name', 'image_url', 'email'])