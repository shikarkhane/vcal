from app import engine

from app.mod_communicate.bl import Message
from app.mod_member.models import User
from app.mod_workday.models import StandinDay

from app.common.util import DateUtil, run_async
from app.common.constants import Email, DayType
from app.email_config import ALL_PARENTS, SUPER_ADMIN


def send(email, type, metricList):
    Message(email, type, metricList).send()


def getVikarieUserId(group_id, dateOfSummon):
    res = engine.query(StandinDay).filter(StandinDay.group_id == group_id, StandinDay.standin_date == dateOfSummon) \
        .all(attributes=['standin_user_id'])
    return res[0]['standin_user_id']


def getEmail(userId):
    res = engine.query(User).filter(User.id == userId) \
        .all(attributes=['email'])
    return res[0]['email']


def notify_unbooked_to_admin(adminEmail, datesAsText):
    send(adminEmail, Email.UNBOOKED_IN_30_DAYS, [datesAsText])

def notify_upcoming_week_to_admin(adminEmail, datesAsText):
    send(adminEmail, Email.UPCOMING_7_DAYS, [datesAsText])


def notify_summon(group_id, dateOfSummon):
    humanDate = DateUtil().getHumanDate(dateOfSummon)
    userId = getVikarieUserId(group_id, dateOfSummon)
    email = getEmail(userId)
    send(email, Email.SUMMONED, [humanDate])


def notify_booked(userId, dateBooked, isWorkday):
    humanDate = DateUtil().getHumanDate(dateBooked)
    dayType = DayType.VIKARIE_DAG
    if (isWorkday):
        dayType = DayType.ARBETS_DAG
    email = getEmail(userId)
    send(email, Email.BOOKED, [humanDate, dayType])

def notify_switch_broadcast(userId, dateBooked, isWorkday):
    humanDate = DateUtil().getHumanDate(dateBooked)
    dayType = DayType.VIKARIE_DAG
    if (isWorkday):
        dayType = DayType.ARBETS_DAG
    familyname = getEmail(userId).split('@')[0]
    email = ALL_PARENTS
    send(email, Email.SWITCH_BROADCAST, [familyname, dayType, humanDate])


def notify_switch(userId, dateBooked, isWorkday):
    humanDate = DateUtil().getHumanDate(dateBooked)
    dayType = DayType.VIKARIE_DAG
    if (isWorkday):
        dayType = DayType.ARBETS_DAG
    email = getEmail(userId)
    send(email, Email.SWITCH, [humanDate, dayType])


def notify_switched(userId, dateBooked, isWorkday, userIdWhoTookSwitchDate):
    humanDate = DateUtil().getHumanDate(dateBooked)
    dayType = DayType.VIKARIE_DAG
    if (isWorkday):
        dayType = DayType.ARBETS_DAG
    email = getEmail(userId)
    switchUserEmail = getEmail(userIdWhoTookSwitchDate)
    send(email, Email.SWITCHED, [humanDate, dayType, switchUserEmail])


def notify_term_open(termName, termStartDate, termEndDate):
    email = ALL_PARENTS
    termDetails = "{0} till {1}".format(termStartDate, termEndDate)
    send(email, Email.TERM_OPEN, [termName, termDetails])


def notify_term_edited(termName, termStartDate, termEndDate):
    email = ALL_PARENTS
    termDetails = "{0} till {1}".format(termStartDate, termEndDate)
    send(email, Email.TERM_EDITED, [termName, termDetails])

def send_email_test():
    send(SUPER_ADMIN, Email.SUMMONED, ['test'])