from base.mod_group.bl import getAllGroups, getGroupByDomain
from base.mod_workday.bl import getOpenStandin, getOpenWorkday, \
    getStandinVikarieForNextXDays, getWorkdayVikarieForNextXDays
from base.mod_communicate.bl import Message
from base.common.bl import getGroupAdmins
from base.common.notify import notify_unbooked_to_admin, notify_upcoming_week_to_vikarie, \
    remind_update_showups
from base.common.util import DateUtil, UserUtil
import logging
from base import create_app_for_triggered_event
import os as operative_system

# Log everything, and send it to stderr.
logging.basicConfig(filename="error.log",level=logging.INFO,format='%(asctime)s %(message)s')



def get_app_context():
    app = create_app_for_triggered_event()
    app.app_context().push()

def unbooked_dates():
    '''If there are unbooked dates in next 30 days,
    after 2 days of term modification,
    send alert to admin'''

    get_app_context()

    #get group gomorronsol only
    groupId = getGroupByDomain('gomorronsol.net')[0]["domain"]
    groupAdmins = getGroupAdmins(groupId)

    if groupAdmins:
        os = [i['standin_date'] for i in getOpenStandin(groupId) if not DateUtil().isAWeekend(i['standin_date']) \
              and DateUtil().isFutureDate(i['standin_date'])]
        ow = [i['work_date'] for i in getOpenWorkday(groupId) if not DateUtil().isAWeekend(i['work_date']) \
              and DateUtil().isFutureDate(i['work_date'])]

        if os or ow:
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

    get_app_context()

    #get group gomorronsol only
    groupId = getGroupByDomain('gomorronsol.net')[0]["domain"]
    groupAdmins = getGroupAdmins(groupId)
    daycare_chief = operative_system.environ['DAY_CARE_CHIEF_EMAIL']

    if groupAdmins:
        os = [[i.standin_date, i.standin_user_id] for i in getStandinVikarieForNextXDays(groupId,0,8)]
        ow = [[i.work_date, i.standin_user_id] for i in getWorkdayVikarieForNextXDays(groupId,0,8)]

        if os or ow:
            du = DateUtil()
            uu = UserUtil(groupId)
            fn_date = lambda x: du.getHumanDate(x)
            # fn_name = lambda x: uu.getName(x).encode('utf-8').strip()
            fn_name = lambda x: uu.getName(x)

            emails = [uu.getEmail(i[1])for i in os] + [uu.getEmail(i[1])for i in ow] + [i['id'] for i in groupAdmins] \
                     + [daycare_chief]

            try:
                datesAsText = "Standins -  " + ",\n".join(["{0} - {1}".format(fn_date(i[0]), fn_name(i[1])) for i in os]) \
                              + "\n\n" + \
                              "Workdays -  " + ",\n".join(["{0} - {1}".format(fn_date(i[0]), fn_name(i[1])) for i in ow])

                datesAsText = datesAsText + '''\n\n\nImportant:\n
                Vikarie (standin) timings: 08:00 to 16:30 \n
                Full Arbetsdag (workday) timings: 08:00 to 16:30 \n
                Half Arbetsdag (workday) timings: 12:45 to 17:00 \n\n
                Please arrive in time to avoid inconveinence to the staff.
                '''

                notify_upcoming_week_to_vikarie('vikarie@gomorronsol.net', datesAsText, emails)
            except Exception as e:
                logging.error(e)
    else:
        logging.info("No admins exists")

def mark_showups_reminder():
    '''send reminder to admins to mark the show ups for the past week'''

    get_app_context()

    #get group gomorronsol only
    groupId = getGroupByDomain('gomorronsol.net')[0]["domain"]
    groupAdmins = getGroupAdmins(groupId)

    if groupAdmins:
        try:
            for admin in groupAdmins:
                remind_update_showups(admin['id'])
        except Exception as e:
            logging.error(e)
    else:
        logging.info("No admins exists")
