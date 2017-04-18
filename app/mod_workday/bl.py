from app import engine
from operator import itemgetter

from app.mod_workday.models import Workday, StandinDay

def getOpenWorkday(group_id):
    w = engine.query(Workday).filter(Workday.group_id == group_id, Workday.standin_user_id == None).all()
    newS = sorted(w, key=itemgetter('work_date'))
    return newS

def getOpenStandin(group_id):
    s = engine.query(StandinDay).filter(StandinDay.group_id == group_id,
                                        StandinDay.standin_user_id == None).all()
    newS = sorted(s, key=itemgetter('standin_date'))
    return newS
