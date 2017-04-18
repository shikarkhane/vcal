from app import engine
from app.mod_member.models import User
from app.common.master_data import E_ROLE

# todo: user-group mapping is pending, this method should get by groupId, role.groupadmin
def getGroupAdmins(group_id):
    res = engine.query(User).filter(User.role == E_ROLE.GroupAdmin).all()