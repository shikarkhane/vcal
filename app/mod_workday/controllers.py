from flask import Flask, render_template, request, redirect, abort, \
    Blueprint
import logging
import calendar
import json
#import datetime
import time
# Import the database object from the main app module
from app import engine
from operator import itemgetter

# Import module models (i.e. User)
from app.mod_workday.models import Workday, Summon, StandinDay
import datetime

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_workday = Blueprint('workday', __name__)


# Log everything, and send it to stderr.
logging.basicConfig(filename="error.log",level=logging.INFO,format='%(asctime)s %(message)s')

from app.common.util import AlchemyEncoder

@mod_workday.route("/workday/<group_id>/", methods=['GET','POST'])
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
            engine.save(w)
            return 'workday was saved'
        elif request.method == 'GET':
            r = engine.query(Workday).filter(Workday.group_id==group_id).all()
            newS = sorted(r, key=itemgetter('work_date'))
            return json.dumps(newS, cls=AlchemyEncoder)
            # return render_template('workday/{0}.html'.format('work-day'))
        else:
            return abort(404)
    except Exception, e:
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

            w = StandinDay( d['group_id'],
                        d['standin_date'],
                        standin_user_id,
                        d['booking_date'])
            engine.save(w)
            return 'standin day was saved'
        elif request.method == 'GET':
            vacant_dates = engine.query(StandinDay).filter(StandinDay.standin_user_id==None).all()
            return json.dumps(vacant_dates)
        else:
            return abort(404)
    except Exception, e:
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

            while startDate <= endDate:
                existStandin = engine.query(StandinDay).filter(StandinDay.group_id == gid,
                                                        StandinDay.booking_date == calendar.timegm(startDate.timetuple())).all()
                if not existStandin:
                    w = StandinDay( gid,
                                calendar.timegm(startDate.timetuple()),
                                standin_user_id,
                                int(time.time()))
                    engine.save(w)
                startDate = startDate + datetime.timedelta(days=1)

            return 'standin day range was saved'
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")

@mod_workday.route("/summon/<group_id>/", methods=['GET','POST'])
def summon(group_id):
    try:
        if request.method == 'POST':
            d = request.get_json()
            w = Summon(d['created_by_id'], group_id,
                       d['work_date'],
                       d['from_time'], d['to_time'])
            engine.save(w)
            return 'summon was saved'
        elif request.method == 'GET':
            r = engine.query(Summon).filter(Summon.group_id==group_id).all()
            newS = sorted(r, key=itemgetter('work_date'))
            return json.dumps(newS, cls=AlchemyEncoder)
            #return render_template('workday/{0}.html'.format('summon'))
        else:
            return abort(404)
    except Exception, e:
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
            return 'removed standin booking'
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")
@mod_workday.route("/workday/<workday_id>/", methods=['PUT'])
def unbook_workday(workday_id):
    try:
        if request.method == 'PUT':
            r = engine.query(Workday).filter(Workday.id==workday_id).all()
            if r:
                newR = r[0]
                newR.standin_user_id = None
                newR.booking_date = int(time.time())
                engine.sync(newR)

            return ' workday unbooked'
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")
@mod_workday.route("/summon/<summon_id>/", methods=['DELETE'])
def delete_summon(summon_id):
    try:
        if request.method == 'DELETE':
            engine.query(Summon).filter(Summon.id==summon_id).delete()
            return 'Deleted summon'
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")

@mod_workday.route("/show-ups/<group_id>/date/<chosen_date>/", methods=['GET', 'POST'])
def showup(group_id, chosen_date):
    try:
        gid = group_id
        dt = chosen_date

        if request.method == 'POST':
            d = request.get_json()
            userId = d['userId']
            isWorkday = d['isWorkday']

            if isWorkday:
                r = engine.query(Workday).filter(Workday.group_id == gid, Workday.standin_user_id == userId,
                                                 Workday.work_date == dt).all()
                if r:
                    newR = r[0]
                    newR.has_worked = True
                    engine.save(newR)
            else:
                r = engine.query(StandinDay).filter(StandinDay.group_id == gid, StandinDay.standin_user_id == userId,
                                                    StandinDay.standin_date == dt).all()
                if r:
                    newR = r[0]
                    newR.has_worked = True
                    engine.save(newR)

            return 'showup was saved'
        elif request.method == 'GET':
            w = engine.query(Workday).filter(Workday.group_id==gid, Workday.work_date==dt).all()
            s = engine.query(StandinDay).filter(StandinDay.group_id==gid, StandinDay.standin_date==dt).all()
            w_dumps = json.dumps(w, cls=AlchemyEncoder)
            s_dumps = json.dumps(s, cls=AlchemyEncoder)
            result = {'standin': json.loads(s_dumps), 'workday': json.loads(w_dumps)}
            return json.dumps(result)
            #return render_template('workday/{0}.html'.format('show-ups'), workday_owners=[], standin_owners=[])
        else:
            return abort(404)
    except Exception, e:
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
            is_taken = d['is_taken']

            q_user_id = None
            if is_taken:
                q_user_id = user_id

            dt = chosen_date
            if is_workday:
                # todo: handle inside a db transaction

                w = engine.query(Workday).filter(Workday.group_id==gid, Workday.work_date==dt).all()
                if w:
                    newW = w[0]
                    newW.standin_user_id = q_user_id
                    newW.booking_date = int(time.time())
                    engine.sync(newW)
                else:
                    return 'Workday NOT saved'
            else:
                w = engine.query(StandinDay).filter(StandinDay.group_id==gid, StandinDay.standin_date==dt).all()
                if w:
                    newW = w[0]
                    newW.standin_user_id = q_user_id
                    newW.booking_date = int(time.time())
                    engine.sync(newW)
                else:
                    return 'Standin NOT saved'

            return 'worksignup was saved'
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")

# open days should also list the ones available in Switch day list
@mod_workday.route("/openworkday/<group_id>/", methods=['GET'])
def openworkday(group_id):
    try:
        w = engine.query(Workday).filter(Workday.group_id==group_id, Workday.standin_user_id==None).all()
        newS = sorted(w, key=itemgetter('work_date'))
        return json.dumps(newS, cls=AlchemyEncoder)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")

@mod_workday.route("/openstandin/<group_id>/", methods=['GET'])
def openstandin(group_id):
    try:
        s = engine.query(StandinDay).filter(StandinDay.group_id==group_id, StandinDay.standin_user_id==None).all()
        newS = sorted(s, key=itemgetter('standin_date'))
        return json.dumps(newS, cls=AlchemyEncoder)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")
@mod_workday.route("/myworkday/<group_id>/user/<user_id>/", methods=['GET'])
def myworkday(group_id, user_id):
    try:
        w = engine.query(Workday).filter(Workday.group_id==group_id, Workday.standin_user_id==user_id).all()
        newS = sorted(w, key=itemgetter('work_date'))
        return json.dumps(newS, cls=AlchemyEncoder)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")

@mod_workday.route("/mystandin/<group_id>/user/<user_id>/", methods=['GET'])
def mystandin(group_id, user_id):
    try:
        s = engine.query(StandinDay).filter(StandinDay.group_id==group_id, StandinDay.standin_user_id==user_id).all()
        newS = sorted(s, key=itemgetter('standin_date'))
        return json.dumps(newS, cls=AlchemyEncoder)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")


