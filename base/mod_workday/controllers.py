from flask import Flask, render_template, request, redirect, abort, \
    Blueprint
import logging
import calendar
import json
# import datetime
import time
# Import the database object from the main base module
from base import engine
from operator import itemgetter

from base.common import notify

from base.mod_workday.bl import getOpenStandin, getOpenWorkday

# Import module models (i.e. User)
from base.mod_workday.models import Workday, Summon, StandinDay
import datetime

# Define the blueprint: 'auth', set its url prefix: base.url/auth
mod_workday = Blueprint('workday', __name__)

# Log everything, and send it to stderr.
logging.basicConfig(filename="error.log", level=logging.INFO, format='%(asctime)s %(message)s')

from base.common.util import AlchemyEncoder


@mod_workday.route("/workday/<group_id>/", methods=['GET', 'POST'])
def working_day(group_id):
    try:
        if request.method == 'POST':
            d = request.get_json()

            if not d['standin_user_id']:
                standin_user_id = None
            else:
                standin_user_id = d['standin_user_id']

            w = Workday(d['created_by_id'], group_id,
                        d['work_date'],
                        d['from_time'], d['to_time'], standin_user_id,
                        d['work_date'],
                        d['is_half_day'])
            id = w.id
            engine.save(w)
            return json.dumps({"status": "ok", "message": "workday was created", "id": id})
        elif request.method == 'GET':
            r = engine.query(Workday).filter(Workday.group_id == group_id).all()
            newS = sorted(r, key=itemgetter('work_date'))
            return json.dumps(newS, cls=AlchemyEncoder)
            # return render_template('workday/{0}.html'.format('work-day'))
        else:
            return abort(404)
    except Exception as e:
        logging.exception(e)
        return render_template("oops.html")


@mod_workday.route("/standinday/", methods=['GET', 'POST'])
def standin_day():
    try:
        if request.method == 'POST':

            d = request.get_json()

            if not d['standin_user_id']:
                standin_user_id = None
            else:
                standin_user_id = d['standin_user_id']

            gid = d['group_id']
            standin_date = datetime.datetime.fromtimestamp(d['standin_date'])

            # create if not exists
            existStandin = engine.query(StandinDay).filter(StandinDay.group_id == gid,
                                                           StandinDay.standin_date == calendar.timegm(
                                                               standin_date.timetuple())).all()
            if not existStandin:
                #create
                w = StandinDay(gid,
                               calendar.timegm(standin_date.timetuple()),
                               standin_user_id,
                               d['booking_date'])
                engine.save(w)
                return json.dumps({"status": "ok", "message": "saved"})
            else:
                return json.dumps({"status": "error", "message": "duplicate"})
        elif request.method == 'GET':
            vacant_dates = engine.query(StandinDay).filter(StandinDay.standin_user_id == None).all()
            return json.dumps(vacant_dates)
        else:
            return abort(404)
    except Exception as e:
        logging.exception(e)
        return render_template("oops.html")


@mod_workday.route("/standindayrange/", methods=['POST'])
def standin_range():
    '''create entries of standin days without any standin user'''
    try:
        if request.method == 'POST':

            d = request.get_json()
            gid = d['group_id']
            standin_user_id = None
            startDate = datetime.datetime.fromtimestamp(d['start_date'])
            endDate = datetime.datetime.fromtimestamp(d['end_date'])

            items_to_save = []

            existingStandins = engine.query(StandinDay).filter(StandinDay.group_id == gid,
                                                            StandinDay.standin_date >= calendar.timegm(
                                                                startDate.timetuple()),
                                                            StandinDay.standin_date <= calendar.timegm(
                                                                endDate.timetuple())
                                                            ).all()
            dictExistingStandinDates = {x.standin_date : 1 for x in existingStandins}

            while startDate <= endDate:
                if not dictExistingStandinDates.get(calendar.timegm(startDate.timetuple())):
                    w = StandinDay(gid,
                                   calendar.timegm(startDate.timetuple()),
                                   standin_user_id,
                                   int(time.time()))
                    items_to_save.append(w)
                startDate = startDate + datetime.timedelta(days=1)

            if items_to_save:
                engine.save(items_to_save)

            return json.dumps({"status": "ok", "message": "saved"})
        else:
            return abort(404)
    except Exception as e:
        logging.exception(e)
        return render_template("oops.html")


@mod_workday.route("/summon/<group_id>/", methods=['GET', 'POST'])
def summon(group_id):
    try:
        if request.method == 'POST':
            d = request.get_json()
            w = Summon(d['created_by_id'], group_id,
                       d['work_date'],
                       d['from_time'], d['to_time'])
            id = w.id
            engine.save(w)
            notify.notify_summon(group_id, d['work_date'])
            return json.dumps({"status": "ok", "message": "saved", "id": id})
        elif request.method == 'GET':
            r = engine.query(Summon).filter(Summon.group_id == group_id).all()
            newS = sorted(r, key=itemgetter('work_date'))
            return json.dumps(newS, cls=AlchemyEncoder)
            # return render_template('workday/{0}.html'.format('summon'))
        else:
            return abort(404)
    except Exception as e:
        logging.exception(e)
        return render_template("oops.html")


@mod_workday.route("/standinday/<standinday_id>/", methods=['PUT'])
def unbook_standin(standinday_id):
    try:
        if request.method == 'PUT':
            r = engine.query(StandinDay).filter(StandinDay.id == standinday_id).all()
            if r:
                newR = r[0]
                newR.standin_user_id = None
                newR.booking_date = int(time.time())
                engine.sync(newR)
            return json.dumps({"status": "ok", "message": "saved"})
        else:
            return abort(404)
    except Exception as e:
        logging.exception(e)
        return render_template("oops.html")


@mod_workday.route("/workday/<workday_id>/", methods=['PUT'])
def unbook_workday(workday_id):
    try:
        if request.method == 'PUT':
            r = engine.query(Workday).filter(Workday.id == workday_id).all()
            if r:
                newR = r[0]
                newR.standin_user_id = None
                newR.booking_date = int(time.time())
                engine.sync(newR)

            return json.dumps({"status": "ok", "message": "saved"})
        else:
            return abort(404)
    except Exception as e:
        logging.exception(e)
        return render_template("oops.html")


@mod_workday.route("/summon/<summon_id>/", methods=['DELETE'])
def delete_summon(summon_id):
    try:
        if request.method == 'DELETE':
            engine.query(Summon).filter(Summon.id == summon_id).delete()
            return json.dumps({"status": "ok", "message": "saved"})
        else:
            return abort(404)
    except Exception as e:
        logging.exception(e)
        return render_template("oops.html")


@mod_workday.route("/workday/<workday_id>/", methods=['DELETE'])
def delete_workday(workday_id):
    try:
        if request.method == 'DELETE':
            engine.query(Workday).filter(Workday.id == workday_id).delete()
            return json.dumps({"status": "ok", "message": "saved"})
        else:
            return abort(404)
    except Exception as e:
        logging.exception(e)
        return render_template("oops.html")


@mod_workday.route("/no-show-ups/<group_id>/date/<chosen_date>/", methods=['GET', 'POST'])
def noshowup(group_id, chosen_date):
    try:
        gid = group_id
        dt = chosen_date

        if request.method == 'POST':
            d = request.get_json()
            userId = d['userId']
            isWorkday = d['isWorkday']

            #field name has_not_worked is wrongly named. it should be has worked instead.
            if isWorkday:
                r = engine.query(Workday).filter(Workday.group_id == gid, Workday.standin_user_id == userId,
                                                 Workday.work_date == dt).all()
                if r:
                    newR = r[0]
                    newR.has_not_worked = True
                    engine.save(newR)
            else:
                r = engine.query(StandinDay).filter(StandinDay.group_id == gid, StandinDay.standin_user_id == userId,
                                                    StandinDay.standin_date == dt).all()
                if r:
                    newR = r[0]
                    newR.has_not_worked = True
                    engine.save(newR)

            return json.dumps({"status": "ok", "message": "saved"})
        elif request.method == 'GET':
            w = engine.query(Workday).filter(Workday.group_id == gid, Workday.work_date == dt).all()
            s = engine.query(StandinDay).filter(StandinDay.group_id == gid, StandinDay.standin_date == dt).all()
            w_dumps = json.dumps(w, cls=AlchemyEncoder)
            s_dumps = json.dumps(s, cls=AlchemyEncoder)
            result = {'standin': json.loads(s_dumps), 'workday': json.loads(w_dumps)}
            return json.dumps(result)
            # return render_template('workday/{0}.html'.format('show-ups'), workday_owners=[], standin_owners=[])
        else:
            return abort(404)
    except Exception as e:
        logging.exception(e)
        return render_template("oops.html")


@mod_workday.route("/work-sign-up/<group_id>/", methods=['GET', 'POST'])
def worksignup(group_id):
    try:
        # todo do not let user deselect a chosen date X days from that date
        d = request.get_json()
        gid = group_id

        if request.method == 'POST':
            user_id = d['user_id']
            chosen_date = d['chosen_date']
            is_workday = d['is_workday']

            id = None
            dt = chosen_date

            if is_workday:
                # todo: handle inside a db transaction

                w = engine.query(Workday).filter(Workday.group_id == gid, Workday.work_date == dt).all()
                if w:
                    user_already_took_an_instance_flag = False
                    # since there can be multiple instances of workday on same date like planning day
                    for x in w:
                        #check if user already took one instance of this workday
                        if x.standin_user_id == user_id:
                            user_already_took_an_instance_flag = True

                    if not user_already_took_an_instance_flag:
                        for newW in w:
                            if not newW.standin_user_id:
                                newW.standin_user_id = user_id
                                newW.booking_date = int(time.time())
                                id = newW.id
                                engine.sync(newW)
                                notify.notify_booked(user_id, dt, is_workday)
                                user_already_took_an_instance_flag = True
                                break

                    if not user_already_took_an_instance_flag:
                        return abort(409)
                else:
                    return json.dumps({"status": "ok", "message": "workday doesnot exist"})
            else:

                w = engine.query(StandinDay).filter(StandinDay.group_id == gid, StandinDay.standin_date == dt).all()
                if w:
                    newW = w[0]
                    if not newW.standin_user_id:
                        newW.standin_user_id = user_id
                        newW.booking_date = int(time.time())
                        id = newW.id
                        engine.sync(newW)
                        notify.notify_booked(user_id, dt, is_workday)
                    else:
                        return abort(409)
                else:
                    return json.dumps({"status": "ok", "message": "standin not found"})

            return json.dumps({"status": "ok", "message": "saved", "id": id})
        else:
            return abort(404)
    except Exception as e:
        logging.exception(e)
        return render_template("oops.html")


@mod_workday.route("/on-switch-work-sign-up/<group_id>/", methods=['POST'])
def onswitch_worksignup(group_id):
    try:
        # todo do not let user deselect a chosen date X days from that date
        d = request.get_json()
        gid = group_id

        if request.method == 'POST':
            user_id = d['user_id']
            chosen_date = d['chosen_date']
            is_workday = d['is_workday']
            standin_user_id = d['standinUserId']

            dt = chosen_date
            if is_workday:
                # todo: handle inside a db transaction

                w = engine.query(Workday).filter(Workday.group_id == gid, Workday.work_date == dt).all()
                if w:
                    newW = w[0]
                    # important for concurrent updates
                    if newW.standin_user_id == standin_user_id:
                        newW.standin_user_id = user_id
                        newW.booking_date = int(time.time())
                        id = newW.id
                        engine.sync(newW)
                        notify.notify_switched(standin_user_id, dt, is_workday, user_id)
                    else:
                        return abort(409)
                else:
                    return json.dumps({"status": "ok", "message": "saved", "id": id})
            else:
                w = engine.query(StandinDay).filter(StandinDay.group_id == gid, StandinDay.standin_date == dt).all()
                if w:
                    newW = w[0]
                    # important for concurrent updates
                    if newW.standin_user_id == standin_user_id:
                        newW.standin_user_id = user_id
                        newW.booking_date = int(time.time())
                        id = newW.id
                        engine.sync(newW)
                        notify.notify_switched(standin_user_id, dt, is_workday, user_id)
                    else:
                        return abort(409)
                else:
                    return json.dumps({"status": "ok", "message": "saved", "id": id})

            return 'on switch - worksignup was saved'
        else:
            return abort(404)
    except Exception as e:
        logging.exception(e)
        return render_template("oops.html")


@mod_workday.route("/openworkday/<group_id>/", methods=['GET'])
def openworkday(group_id):
    try:
        open_days = getOpenWorkday(group_id)
        return json.dumps(open_days, cls=AlchemyEncoder)
    except Exception as e:
        logging.exception(e)
        return render_template("oops.html")


@mod_workday.route("/openstandin/<group_id>/", methods=['GET'])
def openstandin(group_id):
    try:
        open_days = getOpenStandin(group_id)
        return json.dumps(open_days, cls=AlchemyEncoder)
    except Exception as e:
        logging.exception(e)
        return render_template("oops.html")


@mod_workday.route("/myworkday/<group_id>/user/<user_id>/", methods=['GET'])
def myworkday(group_id, user_id):
    try:
        w = engine.query(Workday).filter(Workday.group_id == group_id, Workday.standin_user_id == user_id).all()
        newS = sorted(w, key=itemgetter('work_date'))
        return json.dumps(newS, cls=AlchemyEncoder)
    except Exception as e:
        logging.exception(e)
        return render_template("oops.html")


@mod_workday.route("/mystandin/<group_id>/user/<user_id>/", methods=['GET'])
def mystandin(group_id, user_id):
    try:
        s = engine.query(StandinDay).filter(StandinDay.group_id == group_id,
                                            StandinDay.standin_user_id == user_id).all()
        newS = sorted(s, key=itemgetter('standin_date'))
        return json.dumps(newS, cls=AlchemyEncoder)
    except Exception as e:
        logging.exception(e)
        return render_template("oops.html")


@mod_workday.route("/nonopenworkday/<group_id>/", methods=['GET'])
def nonopenworkday(group_id):
    try:
        w = engine.query(Workday).filter(Workday.group_id == group_id, Workday.standin_user_id != None).all()
        newS = sorted(w, key=itemgetter('work_date'))
        return json.dumps(newS, cls=AlchemyEncoder)
    except Exception as e:
        logging.exception(e)
        return render_template("oops.html")


@mod_workday.route("/nonopenstandin/<group_id>/", methods=['GET'])
def nonopenstandin(group_id):
    try:
        s = engine.query(StandinDay).filter(StandinDay.group_id == group_id, StandinDay.standin_user_id != None).all()
        newS = sorted(s, key=itemgetter('standin_date'))
        return json.dumps(newS, cls=AlchemyEncoder)
    except Exception as e:
        logging.exception(e)
        return render_template("oops.html")
