from base import engine
from operator import itemgetter
import datetime
import calendar

from base.mod_workday.models import Workday, StandinDay

def getOpenWorkday(group_id):
    w = engine.query(Workday).filter(Workday.group_id == group_id, Workday.standin_user_id == None).all()
    newS = sorted(w, key=itemgetter('work_date'))
    return newS

def getOpenStandin(group_id):
    s = engine.query(StandinDay).filter(StandinDay.group_id == group_id,
                                        StandinDay.standin_user_id == None).all()
    newS = sorted(s, key=itemgetter('standin_date'))
    return newS

def getWorkdayVikarieForNextXDays(group_id, start_after_x_days = 2, next_x_days = 5):
    '''with default parameters, if job is executed on friday, it should return weekdays'''
    # todo : make a utility to return next week start and end dates
    date_start = datetime.datetime.now().date() + datetime.timedelta(days= start_after_x_days + 1)
    date_end = date_start + datetime.timedelta(days=next_x_days + 1)

    epoch_start = calendar.timegm(date_start.timetuple())
    epoch_end = calendar.timegm(date_end.timetuple())

    w = engine.query(Workday).filter(Workday.group_id == group_id,
                                     Workday.standin_user_id != None,
                                     Workday.work_date >= epoch_start).all()
    newS = sorted(w, key=itemgetter('work_date'))
    return [i for i in newS if i.work_date < epoch_end]

def getStandinVikarieForNextXDays(group_id, start_after_x_days = 2, next_x_days = 5):
    '''with default parameters, if job is executed on friday, it should return weekdays'''
    # todo : make a utility to return next week start and end dates
    date_start = datetime.datetime.now().date() + datetime.timedelta(days= start_after_x_days + 1)
    date_end = date_start + datetime.timedelta(days=next_x_days + 1)

    epoch_start = calendar.timegm(date_start.timetuple())
    epoch_end = calendar.timegm(date_end.timetuple())

    s = engine.query(StandinDay).filter(StandinDay.group_id == group_id,
                                        StandinDay.standin_user_id != None,
                                        StandinDay.standin_date >= epoch_start).all()
    newS = sorted(s, key=itemgetter('standin_date'))
    return [i for i in newS if i.standin_date < epoch_end]

