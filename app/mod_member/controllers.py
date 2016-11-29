from flask import Flask, render_template, request, redirect, abort, \
    Blueprint, g
import logging
import json

# Import the database object from the main app module
from app import db


from app.mod_member.models import Invite, Member

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_group = Blueprint('member', __name__)


# Log everything, and send it to stderr.
logging.basicConfig(filename="error.log",level=logging.INFO,format='%(asctime)s %(message)s')

@mod_group.before_request
def before():
    if request.view_args and 'lang_code' in request.view_args:
        if request.view_args['lang_code'] not in ('sv', 'en'):
            return abort(404)
        g.current_lang = request.view_args['lang_code']
        request.view_args.pop('lang_code')

@mod_group.route("/<lang_code>/invite/", methods=['POST', 'GET'])
def invite():
    # create a group, group_type, group_owner
    try:
        if request.method == 'POST':
            d = request.get_json()
            gid = d['group_id']
            emails = d['emails']
            for email in emails:
                # todo: add random token number/string
                inv = Invite(email, gid, '1')
                db.session.add(inv)
            db.session.commit()
            return 'invite list saved'
        elif request.method == 'GET':
            return render_template('member/{0}.html'.format('invite'))
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")

@mod_group.route("/<lang_code>/member/", methods=['POST', 'GET'])
def member():
    try:
        if request.method == 'POST':
            d = request.get_json()
            group_id = d['group_id']

            add_users = d['new_user_ids']
            for u in add_users:
                x = Member(group_id, u)
                db.session.add(x)
            db.session.commit()

            removed_ids = d['removed_member_ids']
            for rid in removed_ids:
                Member.query.filter_by(id=rid).delete()
            db.session.commit()
            return 'member list updated'
        elif request.method == 'GET':
            d = request.get_json()
            group_id = d['group_id']
            member_list = Member.query.filter_by(group_id=group_id).all()
            return render_template('member/{0}.html'.format('member'))
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")
