from flask import Flask, render_template, request, redirect, abort, \
    Blueprint
import logging
import json
import datetime

# Import the database object from the main app module
from app import db


# Import module models (i.e. User)
from app.mod_workday.models import Workday, Summon, StandinDay

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
                        datetime.datetime.strptime(d['work_date'], '%Y-%m-%d').date(),
                         d['from_time'], d['to_time'], standin_user_id,
                        datetime.datetime.strptime(d['work_date'], '%Y-%m-%d').date(),
                        d['is_half_day'])
            db.session.add(w)
            db.session.commit()
            return 'workday was saved'
        elif request.method == 'GET':
            r = Workday.query.filter_by(group_id=group_id).all()
            return json.dumps(r, cls=AlchemyEncoder)
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
                        datetime.datetime.strptime(d['standin_date'], '%Y-%m-%d').date(),
                        standin_user_id,
                        datetime.datetime.strptime(d['booking_date'], '%Y-%m-%d').date(),)
            db.session.add(w)
            db.session.commit()
            return 'standin day was saved'
        elif request.method == 'GET':
            vacant_dates = StandinDay.query.filter_by(standin_user_id=None).all()
            return json.dumps(vacant_dates)
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
                       datetime.datetime.strptime(d['work_date'], '%Y-%m-%d').date(),
                       d['from_time'], d['to_time'])
            db.session.add(w)
            db.session.commit()
            return 'summon was saved'
        elif request.method == 'GET':
            r = Summon.query.filter_by(group_id=group_id).all()
            return json.dumps(r, cls=AlchemyEncoder)
            #return render_template('workday/{0}.html'.format('summon'))
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")

@mod_workday.route("/summon/<term_id>/", methods=['DELETE'])
def delete_summon(term_id):
    try:
        if request.method == 'DELETE':
            Summon.query.filter_by(id=term_id).delete()
            db.session.commit()
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
        dt = datetime.datetime.strptime(chosen_date, '%Y-%m-%d')

        if request.method == 'POST':
            d = request.get_json()
            workday_users = d['workday_user_ids']
            standin_users = d['standin_user_ids']

            # update has_worked flag, if user and booking date matches
            for wu in workday_users:
                r = Workday.query.filter_by(group_id=gid, standin_user_id=wu, booking_date=dt).all()
                if r:
                    r.has_worked = True
            for su in standin_users:
                q = StandinDay.query.filter_by(group_id=gid, standin_user_id=su, booking_date=dt).all()
                if q:
                    q.has_worked = True

            return 'showup was saved'
        elif request.method == 'GET':
            w = Workday.query.filter_by(group_id=gid, booking_date=dt).all()
            s = StandinDay.query.filter_by(group_id=gid, booking_date=dt).all()
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

            if is_workday:
                # todo: handle inside a db transaction
                w = Workday.query.filter_by(group_id=gid, work_date=chosen_date,
                                            standin_user_id=q_user_id).first()
                if w:
                    w.standin_user_id = q_user_id
                    w.booking_date = datetime.datetime.utcnow()
                    db.session.commit()
            else:
                w = StandinDay.query.filter_by(group_id=gid, standin_date=chosen_date,
                                            standin_user_id=q_user_id).first()
                if w:
                    w.standin_user_id = q_user_id
                    w.booking_date = datetime.datetime.utcnow()
                    db.session.commit()

            return 'worksignup was saved'
        elif request.method == 'GET':
            user_id = 1
            w = Workday.query.filter_by(group_id=gid, standin_user_id=None).all()
            s = StandinDay.query.filter_by(group_id=gid, standin_user_id=None).all()
            return render_template('workday/{0}.html'.format('work-sign-up'),
                                   workday_owners=[], standin_owners=[])
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")