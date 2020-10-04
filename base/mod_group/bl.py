from base import engine

from base.mod_group.models import Group

def getAllGroups():
    return engine.scan(Group).all()
def getGroupByDomain(domain):
    return engine.query(Group).filter(Group.domain == domain).all()
