from flask import Flask, render_template, request, redirect, abort, \
    Blueprint, g
import logging
import json

# Import the database object from the main app module
from app import db


# Import module models (i.e. User)
from app.mod_group.models import Group

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_group = Blueprint('group', __name__)


# Log everything, and send it to stderr.
logging.basicConfig(filename="error.log",level=logging.INFO,format='%(asctime)s %(message)s')

@mod_group.before_request
def before():
    if request.view_args and 'lang_code' in request.view_args:
        if request.view_args['lang_code'] not in ('sv', 'en'):
            return abort(404)
        g.current_lang = request.view_args['lang_code']
        request.view_args.pop('lang_code')

@mod_group.route("/<lang_code>/group/", methods=['POST', 'GET'])
def group():
    # create a group, group_type, group_owner
    try:
        if request.method == 'POST':
            d = request.get_json()
            g = Group(d['name'], d['type_id'])
            db.session.add(g)
            db.session.commit()
            return 'group saved'
        elif request.method == 'GET':
            return render_template('group/{0}.html'.format('group'))
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")
