from app.mod_group.bl import getAllGroups, getGroupByDomain
from app.mod_workday.bl import getOpenStandin, getOpenWorkday, \
    getStandinVikarieForNextXDays, getWorkdayVikarieForNextXDays
from app.mod_communicate.bl import Message
from app.common.bl import getGroupAdmins
from app.common.notify import notify_unbooked_to_admin
from app.common.util import DateUtil, UserUtil
import logging

# Log everything, and send it to stderr.
logging.basicConfig(filename="error.log",level=logging.INFO,format='%(asctime)s %(message)s')


def unbooked_dates(event, context):
    '''If there are unbooked dates in next 30 days,
    after 2 days of term modification,
    send alert to admin'''

    #get group gomorronsol only
    groupId = getGroupByDomain('gomorronsol.net')[0]["domain"]
    groupAdmins = getGroupAdmins(groupId)

    if groupAdmins:
        os = [i['standin_date'] for i in getOpenStandin(groupId)]
        ow = [i['work_date'] for i in getOpenWorkday(groupId)]

        du = DateUtil()
        fn = lambda x: du.getHumanDate(x)

        datesAsText = "Open Standins -  " + ",\n".join([fn(i) for i in os]) \
                      + "\n\n" + \
                      "Open Workdays -  " + ",\n".join([fn(i) for i in ow])

        for admin in groupAdmins:
            notify_unbooked_to_admin(admin['id'], datesAsText)
    else:
        logging.info("No admins exists")

def weekly_reminder():
    '''send reminder every friday evening to vikarie in upcoming week'''
    #get group gomorronsol only
    groupId = getGroupByDomain('gomorronsol.net')[0]["domain"]
    groupAdmins = getGroupAdmins(groupId)

    if not groupAdmins:
        os = [[i['standin_date'], i['standin_user_id']] for i in getStandinVikarieForNextXDays(groupId,0,7)]
        ow = [[i['work_date'], i['standin_user_id']] for i in getWorkdayVikarieForNextXDays(groupId,0,7)]

        du = DateUtil()
        uu = UserUtil(groupId)
        fn_date = lambda x: du.getHumanDate(x)
        fn_name = lambda x: uu.getName(x)

        datesAsText = "Standins -  " + ",\n".join(["{0} - {1}".format(fn_date(i[0]), fn_name(i[1])) for i in os]) \
                      + "\n\n" + \
                      "Workdays -  " + ",\n".join(["{0} - {1}".format(fn_date(i[0]), fn_name(i[1])) for i in ow])

        for admin in groupAdmins:
            notify_unbooked_to_admin(admin['id'], datesAsText)
    else:
        logging.info("No admins exists")
