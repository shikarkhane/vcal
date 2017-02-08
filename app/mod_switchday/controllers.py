from flask import Flask, render_template, request, redirect, abort, \
    Blueprint
import logging
import json
#import datetime

# Import the database object from the main app module
from app import engine


from app.mod_switchday.models import Switchday
from operator import itemgetter

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_switchday = Blueprint('switchday', __name__)


# Log everything, and send it to stderr.
logging.basicConfig(filename="error.log",level=logging.INFO,format='%(asctime)s %(message)s')

from app.common.util import AlchemyEncoder

@mod_switchday.route("/switchday/<group_id>/user/<user_id>/", methods=['GET', 'POST'])
def manage(group_id, user_id):
    try:
        # todo do not let user deselect a chosen date X days from that date
        gid = group_id

        if request.method == 'POST':
            # only used to offer own date for switching
            d = request.get_json()
            chosen_date = d['chosen_date']
            is_workday = d['is_workday']

            dt = chosen_date
            # todo: handle inside a db transaction
            w = engine.query(Switchday).filter(Switchday.group_id==gid, Switchday.switch_date==dt).all()
            if not w:
                w = Switchday(group_id,
                            d['chosen_date'],
                            d['from_time'], d['to_time'], user_id,
                            d['is_half_day'], is_workday)
                engine.save(w)
            else:
                return abort(409)
            return json.dumps({"status": "ok", "message": "saved"})
        elif request.method == 'GET':
            r = engine.query(Switchday).filter(Switchday.group_id==group_id, Switchday.standin_user_id==user_id).all()
            newS = sorted(r, key=itemgetter('switch_date'))
            return json.dumps(newS, cls=AlchemyEncoder)
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")
@mod_switchday.route("/switchday/<group_id>/standinuser/<standin_user_id>/", methods=['DELETE'])
def delete(group_id, standin_user_id):
    try:
        # todo do not let user deselect a chosen date X days from that date
        gid = group_id

        if request.method == 'DELETE':
            d = request.get_json()
            dt = d['chosen_date']

            engine.query(Switchday).filter(Switchday.group_id==gid, Switchday.switch_date==dt,
                                               Switchday.standin_user_id==standin_user_id).delete()
            return json.dumps({"status": "ok", "message": "saved"})
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")

@mod_switchday.route("/switchday/<group_id>/type/<show_workday>/", methods=['GET'])
def open_switchday(group_id, show_workday):
    try:
        if request.method == 'GET':
            r = []
            if int(show_workday) == 1:
                r = engine.query(Switchday).filter(Switchday.group_id==group_id, Switchday.is_work_day==True).all()
            else:
                r = engine.query(Switchday).filter(Switchday.group_id==group_id, Switchday.is_work_day==False).all()
            newS = sorted(r, key=itemgetter('switch_date'))
            return json.dumps(newS, cls=AlchemyEncoder)
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")
