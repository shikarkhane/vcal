from flask import Flask, render_template, request, redirect, abort, \
    Blueprint, g
import logging
import json

# Import the database object from the main app module
from app import db


# Import module models (i.e. User)
#from app.mod_group.models import Group

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_actionday = Blueprint('actionday', __name__)


# Log everything, and send it to stderr.
logging.basicConfig(filename="error.log",level=logging.INFO,format='%(asctime)s %(message)s')

@mod_actionday.before_request
def before():
    if request.view_args and 'lang_code' in request.view_args:
        if request.view_args['lang_code'] not in ('sv', 'en'):
            return abort(404)
        g.current_lang = request.view_args['lang_code']
        request.view_args.pop('lang_code')

@mod_actionday.route("/<lang_code>/show-ups/", methods=[ 'GET'])
def showup():
    try:
        return render_template('actionday/{0}.html'.format('show-ups'))
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")

@mod_actionday.route("/<lang_code>/work-sign-up/", methods=[ 'GET'])
def worksignup():
    try:
        # todo do not let user deselect a chosen date X days from that date
        return render_template('actionday/{0}.html'.format('work-sign-up'))
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")