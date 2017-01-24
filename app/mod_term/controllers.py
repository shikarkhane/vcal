from flask import Flask, render_template, request, redirect, abort, \
    Blueprint
import logging
import json
import datetime
# Import the database object from the main app module
from app import engine


from app.mod_term.models import Term, Children

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_term = Blueprint('term', __name__)

from app.common.util import AlchemyEncoder

# Log everything, and send it to stderr.
logging.basicConfig(filename="error.log",level=logging.INFO,format='%(asctime)s %(message)s')

@mod_term.route("/term/", methods=['POST', 'GET'])
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
            engine.save(r)
            return 'term saved'
        elif request.method == 'GET':
            return render_template('term/{0}.html'.format('term'))
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")
@mod_term.route("/term_details/<group_id>/", methods=['GET'])
def term_details(group_id):
    try:
        r = engine.query(Term).filter_by(group_id=group_id).all()
        return json.dumps(r, cls=AlchemyEncoder)
        #return json.dumps([{'name': 'vt2016', 'start-date': '2016-09-01', 'end-date': '2016-12-31', 'id': '1'}])
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")

@mod_term.route("/children/<term_id>/", methods=['GET', 'POST'])
def children(term_id):
    try:
        if request.method == 'POST':
            d = request.get_json()
            tid = term_id
            child_count = d['child_count']
            r = Children(tid, child_count)
            engine.query(Children).filter_by(term_id=tid).delete()
            engine.save(r)
            return 'term child count saved'
        elif request.method == 'GET':
            r = engine.query(Children).filter_by(term_id=term_id).all()
            return json.dumps(r, cls=AlchemyEncoder)
            #return render_template('term/{0}.html'.format('children'))
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")