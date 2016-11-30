from flask import Flask, render_template, request, redirect, abort, \
    Blueprint, g
import logging
import json

# Import the database object from the main app module
from app import db


from app.mod_term.models import Term

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_switchday = Blueprint('switchday', __name__)


# Log everything, and send it to stderr.
logging.basicConfig(filename="error.log",level=logging.INFO,format='%(asctime)s %(message)s')

@mod_switchday.before_request
def before():
    if request.view_args and 'lang_code' in request.view_args:
        if request.view_args['lang_code'] not in ('sv', 'en'):
            return abort(404)
        g.current_lang = request.view_args['lang_code']
        request.view_args.pop('lang_code')

@mod_switchday.route("/<lang_code>/switchday/", methods=['POST', 'GET'])
def rule():
    try:
        if request.method == 'POST':
            return 'switch day saved'
        elif request.method == 'GET':
            return render_template('switchday/{0}.html'.format('switchday'))
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")
