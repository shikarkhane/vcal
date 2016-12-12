from flask import Flask, render_template, request, redirect, abort, \
    Blueprint, g
import logging
import json
import datetime

# Import the database object from the main app module
from app import db, get_locale


# Import module models (i.e. User)
from app.mod_workday.models import Workday, Summon, StandinDay

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_workday = Blueprint('workday', __name__)


# Log everything, and send it to stderr.
logging.basicConfig(filename="error.log",level=logging.INFO,format='%(asctime)s %(message)s')



@mod_workday.before_request
def before():
    if request.view_args and 'lang_code' in request.view_args:
        if request.view_args['lang_code'] not in ('sv', 'en'):
            return abort(404)
        g.current_lang  = request.view_args['lang_code']
        request.view_args.pop('lang_code')


@mod_workday.route("/<lang_code>/workday/", methods=['GET','POST'])
def working_day():
    try:
        if request.method == 'POST':
            d = request.get_json()
            w = Workday(d['created_by_id'], d['group_id'],
                        datetime.datetime.strptime(d['work_date'], '%Y-%m-%d').date(),
                        d['standin_count'], d['from_time'], d['to_time'])
            db.session.add(w)
            db.session.commit()
            return 'workday was saved'
        elif request.method == 'GET':
            return render_template('workday/{0}.html'.format('work-day'))
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")

@mod_workday.route("/<lang_code>/standinday/", methods=['GET', 'POST'])
def standin_day():
    try:
        if request.method == 'POST':
            # todo: saving standin_user_id as None is pending.
            d = request.get_json()
            w = StandinDay( d['group_id'],
                        datetime.datetime.strptime(d['standin_date'], '%Y-%m-%d').date(),
                        d['standin_user_id'],
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

@mod_workday.route("/<lang_code>/summon/", methods=['GET','POST'])
def summon():
    try:
        if request.method == 'POST':
            d = request.get_json()
            w = Summon(d['created_by_id'], d['group_id'], d['work_date'], d['from_time'], d['to_time'])
            db.session.add(w)
            db.session.commit()
            return 'summon was saved'
        elif request.method == 'GET':
            return render_template('workday/{0}.html'.format('summon'))
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")
