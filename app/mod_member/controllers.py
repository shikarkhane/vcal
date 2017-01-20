from flask import Flask, render_template, request, redirect, abort, \
    Blueprint
import logging
import json

# Import the database object from the main app module
from app import db


from app.mod_member.models import Invite, Member, User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_member = Blueprint('member', __name__)


# Log everything, and send it to stderr.
logging.basicConfig(filename="error.log",level=logging.INFO,format='%(asctime)s %(message)s')

from app.common.util import AlchemyEncoder


@mod_member.route("/user/", methods=['POST', 'GET'])
def register():
    try:
        if request.method == 'POST':
            d = request.get_json()
            res = User.query.filter_by(email=d['email']).first()
            if not res:
                u = User(d['name'], d['givenName'], d['familyName'], d['email'], None, d['tokenId'], d['imageUrl'])
                db.session.add(u)
                db.session.flush()
                db.session.refresh(u)
                userid = u.id
            else:
                userid = res.id
                res.auth_token = d['tokenId']
                res.image_url = d['imageUrl']
            db.session.commit()
            return json.dumps({'userId': userid})
        elif request.method == 'GET':
            d = request.get_json()
            res = User.query.filter_by(id=d['userId']).first()
            return json.dumps(res, cls=AlchemyEncoder)
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")

@mod_member.route("/invite/", methods=['POST', 'GET'])
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

@mod_member.route("/member/<group_id>/", methods=['POST', 'GET'])
def member(group_id):
    try:
        if request.method == 'POST':
            d = request.get_json()

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
            m = Member.query.filter_by(group_id=group_id).all()
            return json.dumps(m, cls=AlchemyEncoder)
            #return render_template('member/{0}.html'.format('member'))
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")


@mod_member.route("/joingroup/<invite_code>/", methods=['POST'])
def joingroup(invite_code):
    try:
        # todo: user joins a group if invite id matches. for time being we keep this simple
        if request.method == 'POST':
            d = request.get_json()
            group_id = d['group_id']
            user_id = d['group_id']

            x = Member(group_id, user_id)
            db.session.add(x)
            db.session.commit()

            return 'Joined group'
        else:
            return abort(404)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")
