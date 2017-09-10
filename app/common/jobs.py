from app.mod_group.bl import getAllGroups, getGroupByDomain
from app.mod_workday.bl import getOpenStandin, getOpenWorkday
from app.mod_communicate.bl import Message
from app.common.bl import getGroupAdmins
from app.common.notify import notify_unbooked_to_admin
from app.common.util import DateUtil


def unbooked_dates(event, context):
    '''If there are unbooked dates in next 30 days,
    after 2 days of term modification,
    send alert to admin'''

    #get group gomorronsol only
    groupId = getGroupByDomain('gomorronsol.net')[0]["domain"]
    groupAdmins = getGroupAdmins(groupId)
    os = getOpenStandin(groupId)
    ow = getOpenWorkday(groupId)

    fn = lambda x: DateUtil().getHumanDate(x)
    datesAsText = "Open Standins -  " + ",\n".join([fn(i) for i in os]) + "\n\n" + "Open Workdays -  " + ",\n".join([fn(i) for i in ow])

    for admin in groupAdmins:
        notify_unbooked_to_admin(admin['id'], datesAsText)
