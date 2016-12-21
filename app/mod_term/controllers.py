from flask import Flask, render_template, request, redirect, abort, \
    Blueprint, g
import logging
import json
import datetime
# Import the database object from the main app module
from app import db


from app.mod_term.models import Term, Children

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
def term():
    try:
        # todo when a new term is set/updated, add dates in vikariedays table
        if request.method == 'POST':
            d = request.get_json()
            gid = d['group_id']
            name = d['term_name']
            start_dt = datetime.datetime.strptime(d['start_date'], '%Y-%m-%d').date()
            end_dt = datetime.datetime.strptime(d['end_date'], '%Y-%m-%d').date()
            family_spread = json.dumps(d['family_spread'])
            r = Term(gid, name, start_dt, end_dt, family_spread)
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
@mod_term.route("/<lang_code>/term_details/<group_id>/", methods=['GET'])
def term_details(group_id):
    try:
        return json.dumps([{'name': 'vt2016', 'start-date': '2016-09-01', 'end-date': '2016-12-31'}])
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")

@mod_term.route("/<lang_code>/children/", methods=['GET', 'POST'])
def children():
    try:
        if request.method == 'POST':
            d = request.get_json()
            tid = d['term_id']
            child_count = d['child_count']
            r = Children(tid, child_count)
            Children.query.filter_by(term_id=tid).delete()
            db.session.add(r)
            db.session.commit()
            return 'term child count saved'
        elif request.method == 'GET':
            return render_template('term/{0}.html'.format('children'))
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")