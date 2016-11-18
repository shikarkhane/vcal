from flask import Flask, render_template, request, redirect, abort, Blueprint
import logging
import json

# Import the database object from the main app module
from app import db, get_locale


# Import module models (i.e. User)
from app.mod_draft.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_draft = Blueprint('draft', __name__)


# Log everything, and send it to stderr.
logging.basicConfig(filename="error.log",level=logging.INFO,format='%(asctime)s %(message)s')



@mod_draft.before_request
def before():
    if request.view_args and 'lang_code' in request.view_args:
        if request.view_args['lang_code'] not in ('sv', 'en'):
            return abort(404)
        g['current_lang'] = request.view_args['lang_code']
        request.view_args.pop('lang_code')

@mod_draft.route("/")
def root():
    return redirect("/sv/")

@mod_draft.route("/<lang_code>/")
def landing():
    try:
        return render_template('draft/landing.html')
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")

@mod_draft.route("/<lang_code>/dashboard/<usertype>/")
def dashboard(usertype):
    try:
        return render_template('draft/dashboard.html', usertype = usertype)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")

@mod_draft.route("/<lang_code>/template/<template>/")
def anytemplate(template):
    try:
        return render_template('draft/{0}.html'.format(template))
    except Exception, e:
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
# @app.route("/<lang_code>/invite/")
# def invite():
#     # invite by emails
#     return render_template('register.html')
# @app.route("/<lang_code>/members/", methods=['GET','POST'])
# def members():
#     # get all members for a group
#     # post removals or additions to a group
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
