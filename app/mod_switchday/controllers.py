from flask import Flask, render_template, request, redirect, abort, \
    Blueprint
import logging
import json

# Import the database object from the main app module
from app import db


from app.mod_term.models import Term

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_switchday = Blueprint('switchday', __name__)


# Log everything, and send it to stderr.
logging.basicConfig(filename="error.log",level=logging.INFO,format='%(asctime)s %(message)s')

@mod_switchday.route("/switchday/", methods=['POST', 'GET'])
def rule():
    try:
        # todo show Term in the UI, people can choose to term and see the same info
        # split into 2 tabs for vikarie days and arbetsdag
        if request.method == 'POST':
            return 'switch day saved'
        elif request.method == 'GET':
            return render_template('switchday/{0}.html'.format('switchday'))
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")
