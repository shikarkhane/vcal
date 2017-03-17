from flask import render_template, request, abort, \
    Blueprint
import logging
import json

# Import the database object from the main app module
from app import engine


# Import module models (i.e. User)
from app.mod_group.models import Group

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_group = Blueprint('group', __name__)


# Log everything, and send it to stderr.
logging.basicConfig(filename="error.log",level=logging.INFO,format='%(asctime)s %(message)s')

from app.common.util import AlchemyEncoder

@mod_group.route("/group/", methods=['POST', 'GET'])
def group():
    # create a group, group_type, group_owner
    try:
        if request.method == 'POST':
            d = request.get_json()
            g = Group(d['name'], int(d['type_id']))
            engine.save(g)
            return json.dumps({"status": "ok", "message": "saved"})
        elif request.method == 'GET':
            r = engine.scan(Group).all()
            return json.dumps(r, cls=AlchemyEncoder)
            #return render_template('group/{0}.html'.format('group'))
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")
@mod_group.route("/group/<group_id>/", methods=['PUT', 'GET'])
def defaultTermPut(group_id):
    try:
        if request.method == 'PUT':
            d = request.get_json()
            g = engine.get(Group, id=group_id)
            g.default_term_id = d['default_term_id']
            g.sync()
            return json.dumps({"status": "ok", "message": "saved"})
        elif request.method == 'GET':
            g = engine.get(Group, id=group_id)
            return json.dumps(g, cls=AlchemyEncoder)
            #return render_template('group/{0}.html'.format('group'))
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")
