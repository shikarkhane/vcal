from app import engine

from app.mod_communicate.bl import Message
from app.mod_member.models import User

from app.common.util import DateUtil


def send(email, type, metricList):
    Message(email, type, metricList).send()

def getEmail(userId):
    res = engine.query(User).filter(User.id == userId) \
        .all(attributes=['email'])
    return res[0]

def notify_booked(userId, bookingDate, isWorkday):
    humanDate = DateUtil().getHumanDate(bookingDate)
    dayType = 'vikarie'
    if ( isWorkday):
        dayType = 'arbetsdag'
    email = getEmail(userId)

    send(email, 'BOOKED', [humanDate, dayType])

def notify_switch():
    pass
def notify_switched():
    pass
def notify_term_open():
    pass
def notify_term_edited():
    pass

