from flask import Flask, render_template, request, redirect, abort, \
    Blueprint
import logging
import json

# Import the database object from the main app module
from app import engine


from app.mod_rule.models import Rule

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_rule = Blueprint('rule', __name__)


# Log everything, and send it to stderr.
logging.basicConfig(filename="error.log",level=logging.INFO,format='%(asctime)s %(message)s')

from app.common.util import AlchemyEncoder

@mod_rule.route("/rule/<group_id>/term/<term_id>/", methods=['POST', 'GET'])
def rule(group_id, term_id):
    try:
        if request.method == 'POST':
            d = request.get_json()
            gid = group_id
            rule_definition = d['definition']
            r = Rule(gid, term_id, json.dumps(rule_definition))
            engine.query(Rule).filter(Rule.group_id == gid, Rule.term_id == term_id).delete()
            engine.save(r)
            return 'rule saved'
        elif request.method == 'GET':
            r = engine.query(Rule).filter(Rule.group_id==group_id, Rule.term_id==term_id).all()
            if not r:
                return json.dumps({})
            return json.dumps(r[0], cls=AlchemyEncoder)
            #return render_template('rule/{0}.html'.format('rule'))
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")
