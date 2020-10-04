from flask import Flask, render_template, request, redirect, abort, \
    Blueprint
import logging
import json

# Import the database object from the main app module
from app import engine
from app.mod_draft.models import PublicHoliday
from app.common.util import AlchemyEncoder
from operator import itemgetter



# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_draft = Blueprint('draft', __name__)


# Log everything, and send it to stderr.
logging.basicConfig(filename="error.log",level=logging.INFO,format='%(asctime)s %(message)s')



@mod_draft.route("/")
def landing():
    try:
        return render_template('draft/landing.html')
    except Exception as e:
        logging.exception(e)
        return render_template("oops.html")

@mod_draft.route("/holiday/<group_id>/", methods=['GET', 'POST'])
def holiday_day(group_id):
    try:
        if request.method == 'POST':
            d = request.get_json()

            w = PublicHoliday(d['created_by_id'], group_id,
                        d['holiday_date'],
                        False)
            engine.save(w)
            return json.dumps({"status": "ok", "message": "holiday was created"})
        elif request.method == 'GET':
            r = engine.query(PublicHoliday).filter(PublicHoliday.group_id == group_id).all(attributes=['holiday_date', 'id'])
            newS = sorted(r, key=itemgetter('holiday_date'))
            return json.dumps(newS, cls=AlchemyEncoder)
            # return render_template('workday/{0}.html'.format('work-day'))
        else:
            return abort(404)
    except Exception as e:
        logging.exception(e)
        return render_template("oops.html")

@mod_draft.route("/holiday/<holiday_id>/", methods=['DELETE'])
def unbook_workday(holiday_id):
    try:
        if request.method == 'DELETE':
            engine.query(PublicHoliday).filter(PublicHoliday.id == holiday_id).delete()
            return json.dumps({"status": "ok", "message": "saved"})
        else:
            return abort(404)
    except Exception as e:
        logging.exception(e)
        return render_template("oops.html")

# @mod_draft.route("/<lang_code>/register/", methods=['POST'])
# def register():
#     # full name, token, password, is_gmail, creation_date, phone numbers
#     return render_template('draft/register.html')
# @app.route("/<lang_code>/group/<groupname>/register/", methods=['POST'])
# def register_via_invite():
#     # full name, token, password, is_gmail, creation_date, phone numbers
#     return render_template('register.html')
# @app.route("/<lang_code>/group/getall/")
# def groups():
#     # return all groups user belongs to along with is_admin info
#     return render_template('register.html')
# @app.route("/<lang_code>/term/<termname>/", methods=['GET','POST','DEL'])
# def term(termname):
#     # groupname, term name, start, end, expected_kids_count, is_open
#     # check if group has members not signed up yet, notify admin
#     # notify that term is open and force to confirm kid count on login
#     # dont let anyone sign-up for dates untill everyone has done kid count as expected kid count
#     return render_template('register.html')
# @app.route("/<lang_code>/terms/")
# def terms():
#     # return all terms for a <group>
#     return render_template('register.html')

# @app.route("/<lang_code>/summon/")
# def summon():
#     # In <group>, summon X number of people on D date for <half day> with <time notes>
#     # Inform stand-in via sms
#     # More than stand-in needed, inform all admins in group with list of probable people
#     # they can call to.
#     return render_template('register.html')
# @app.route("/<lang_code>/showups/", methods=['GET','POST'])
# def showups():
#     # who all showed up to work today i.e. usernames which showed up.
#     # groupname, showup_username, username_of_confirmer
#     return render_template('register.html')
# @app.route("/<lang_code>/children/", methods=['GET','POST','DEL'])
# def children_per_term():
#     # parent, term name, children count
#     return render_template('register.html')
# @app.route("/<lang_code>/public_holiday/", methods=['GET','POST'])
# def public_holiday():
#     # groupname, public holday(s)
#     return render_template('register.html')
# @app.route("/<lang_code>/working_day/", methods=['GET','POST'])
# def working_day():
#     # groupname, working day, number of heads needed, time in notes
#     return render_template('register.html')
# @app.route("/<lang_code>/choose_day/", methods=['GET','POST'])
# def choose_day():
#     # dont let anyone sign-up for dates untill everyone has done kid count as expected kid count
#     # Show visual overlay on sign-up button, explaining the reason for wait
#     # groupname, username, date
#     return render_template('register.html')
# @app.route("/<lang_code>/next_available_day/<count>/workday/<is_workday>/")
# def next_available_day(count, is_workday):
#     # groupname, username, term
#     return render_template('register.html')
# @app.route("/<lang_code>/term_work_status/")
# def term_work_status():
#     # groupname, username, term
#     return render_template('register.html')
