from flask import Flask, render_template, request, redirect, abort, \
    Blueprint
import logging
import json

# Import the database object from the main app module
from app import engine

from app.mod_communicate.bl import Message

from app.mod_communicate.models import EmailNotify

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_communicate = Blueprint('communicate', __name__)


# Log everything, and send it to stderr.
logging.basicConfig(filename="error.log",level=logging.INFO,format='%(asctime)s %(message)s')

from app.common.util import AlchemyEncoder

@mod_communicate.route("/communicate/", methods=['POST'])
def communicate():
    try:
        if request.method == 'POST':
            d = request.get_json()
            email = d['email']
            type = d['type']
            metrics = d['metrics']
            r = EmailNotify(email, type)
            engine.save(r)
            return json.dumps({"status": "ok", "message": "saved"})
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")
