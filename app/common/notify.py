from app import engine

from app.mod_communicate.bl import Message
from app.mod_member.models import User

from app.common.util import DateUtil


def send(email, type, metricList):
    Message(email, type, metricList).send()

def getEmail(userId):
    res = engine.query(User).filter(User.id == userId) \
        .all(attributes=['email'])
    return res[0]['email']

def notify_unbooked_to_admin(adminUserId, datesAsText):
    email = getEmail(adminUserId)
    send(email, 'UNBOOKED_IN_30_DAYS', [datesAsText])

def notify_booked(userId, bookingDate, isWorkday):
    humanDate = DateUtil().getHumanDate(bookingDate)
    dayType = 'vikarie'
    if ( isWorkday):
        dayType = 'arbetsdag'
    email = getEmail(userId)

    send(email, 'BOOKED', [humanDate, dayType])

def notify_switch(userId, bookingDate, isWorkday):
    humanDate = DateUtil().getHumanDate(bookingDate)
    dayType = 'vikarie'
    if (isWorkday):
        dayType = 'arbetsdag'
    email = getEmail(userId)

    send(email, 'SWITCH', [humanDate, dayType])

def notify_switched(userId, bookingDate, isWorkday, userIdWhoTookSwitchDate):
    humanDate = DateUtil().getHumanDate(bookingDate)
    dayType = 'vikarie'
    if (isWorkday):
        dayType = 'arbetsdag'
    email = getEmail(userId)
    switchUserEmail = getEmail(userIdWhoTookSwitchDate)

    send(email, 'SWITCHED', [humanDate, dayType, switchUserEmail])

def notify_term_open(termName, termStartDate, termEndDate):
    email = 'parents@gomorronsol.net'
    termDetails = "{0} till {1}".format(termStartDate, termEndDate)
    send(email, 'TERM_OPEN', [termName, termDetails])

def notify_term_edited():
    email = 'parents@gomorronsol.net'
    termDetails = "{0} till {1}".format(termStartDate, termEndDate)
    send(email, 'TERM_EDITED', [termName, termDetails])

