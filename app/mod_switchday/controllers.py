from flask import Flask, render_template, request, redirect, abort, \
    Blueprint
import logging
import json
import datetime

# Import the database object from the main app module
from app import db


from app.mod_switchday.models import Switchday

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_switchday = Blueprint('switchday', __name__)


# Log everything, and send it to stderr.
logging.basicConfig(filename="error.log",level=logging.INFO,format='%(asctime)s %(message)s')

from app.common.util import AlchemyEncoder

@mod_switchday.route("/switchday/<group_id>/user/<user_id>/", methods=['GET', 'POST', 'DELETE'])
def manage(group_id, user_id):
    try:
        # todo do not let user deselect a chosen date X days from that date
        gid = group_id

        if request.method == 'POST':
            # only used to offer own date for switching
            d = request.get_json()
            chosen_date = d['chosen_date']
            is_workday = d['is_workday']

            dt = datetime.datetime.strptime(chosen_date, '%Y-%m-%d')
            # todo: handle inside a db transaction
            w = Switchday.query.filter_by(group_id=gid, switch_date=dt).first()
            if not w:
                w = Switchday(group_id,
                            datetime.datetime.strptime(d['chosen_date'], '%Y-%m-%d').date(),
                            d['from_time'], d['to_time'], user_id,
                            d['is_half_day'], is_workday)
                db.session.add(w)
                db.session.commit()
            else:
                return abort(409)
            return 'switchday was saved'
        elif request.method == 'GET':
            r = Switchday.query.filter_by(group_id=group_id, standin_user_id=user_id).all()
            return json.dumps(r, cls=AlchemyEncoder)
        elif request.method == 'DELETE':
            d = request.get_json()
            chosen_date = d['chosen_date']
            dt = datetime.datetime.strptime(chosen_date, '%Y-%m-%d')

            w = Switchday.query.filter_by(group_id=gid, switch_date=dt, standin_user_id=user_id).delete()
            db.session.commit()
            return 'switchday was deleted'
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")
@mod_switchday.route("/switchday/<group_id>/type/<show_workday>/", methods=['GET'])
def open_switchday(group_id, show_workday):
    try:
        gid = group_id

        if request.method == 'GET':
            r = []
            if show_workday:
                r = Switchday.query.filter_by(group_id=group_id, is_work_day=True).all()
            else:
                r = Switchday.query.filter_by(group_id=group_id, is_work_day=False).all()
            return json.dumps(r, cls=AlchemyEncoder)
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")
