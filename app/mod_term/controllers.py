from flask import Flask, render_template, request, redirect, abort, \
    Blueprint, g
import logging
import json

# Import the database object from the main app module
from app import db


from app.mod_term.models import Term

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_term = Blueprint('term', __name__)


# Log everything, and send it to stderr.
logging.basicConfig(filename="error.log",level=logging.INFO,format='%(asctime)s %(message)s')

@mod_term.before_request
def before():
    if request.view_args and 'lang_code' in request.view_args:
        if request.view_args['lang_code'] not in ('sv', 'en'):
            return abort(404)
        g.current_lang = request.view_args['lang_code']
        request.view_args.pop('lang_code')

@mod_term.route("/<lang_code>/term/", methods=['POST', 'GET'])
def rule():
    try:
        # todo when a new term is set/updated, add dates in vikariedays table
        if request.method == 'POST':
            d = request.get_json()
            gid = d['group_id']
            name = d['term_name']
            family_spread = d['family_spread']
            r = Term(gid, name, family_spread)
            db.session.add(r)
            db.session.commit()
            return 'term saved'
        elif request.method == 'GET':
            return render_template('term/{0}.html'.format('term'))
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")

@mod_term.route("/<lang_code>/children/", methods=['GET'])
def children():
    try:
        return render_template('term/{0}.html'.format('term'))
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")
