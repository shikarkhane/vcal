from flask import Flask, render_template, request, redirect, abort, \
    Blueprint
import logging
import json

# Import the database object from the main base module
from base import engine


from base.mod_member.models import Invite, Member, User

# Define the blueprint: 'auth', set its url prefix: base.url/auth
mod_member = Blueprint('member', __name__)


# Log everything, and send it to stderr.
logging.basicConfig(filename="error.log",level=logging.INFO,format='%(asctime)s %(message)s')

from base.common.util import AlchemyEncoder


@mod_member.route("/user/", methods=['POST', 'GET'])
def register():
    try:
        if request.method == 'POST':
            d = request.get_json()
            res = engine.query(User).filter( User.email == d['email']).all()
            if not res:
                u = User(d['name'], d['givenName'], d['familyName'], d['email'], None, d['tokenId'], d['imageUrl'])
                engine.save(u)
                userid = u.id
                role = u.role
                isActive = u.is_active
            else:
                newR = res[0]
                userid = newR.id
                role = newR.role
                isActive = newR.is_active
                newR.auth_token = d['tokenId']
                newR.image_url = d['imageUrl']
                engine.sync(newR)
            return json.dumps({'userId': userid, 'role': role, 'isActive': isActive})
        elif request.method == 'GET':
            d = request.get_json()
            res = engine.query(User).filter(User.id == d['userId']).all()
            return json.dumps(res, cls=AlchemyEncoder)
        else:
            return abort(404)
    except Exception as e:
        logging.exception(e)
        return render_template("oops.html")

@mod_member.route("/user/<user_id>/", methods=['GET'])
def getUser(user_id):
    try:
        if request.method == 'GET':
            res = engine.query(User).filter(User.id == user_id)\
                .all(attributes=['id', 'name', 'given_name', 'family_name', 'image_url', 'role', 'is_active'])
            return json.dumps(res[0], cls=AlchemyEncoder)
        else:
            return abort(404)
    except Exception as e:
        logging.exception(e)
        return render_template("oops.html")

@mod_member.route("/alluser/", methods=['GET'])
def getAllUsers():
    '''get userid, name and img url for all users'''
    try:
        # todo: filter this by member of a group id
        if request.method == 'GET':
            res = engine.scan(User).all(attributes=['id', 'name', 'given_name', 'family_name', 'image_url'])
            return json.dumps(res, cls=AlchemyEncoder)
        else:
            return abort(404)
    except Exception as e:
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
                engine.save(inv)
            return json.dumps({"status": "ok", "message": "saved"})
        elif request.method == 'GET':
            return render_template('member/{0}.html'.format('invite'))
        else:
            return abort(404)
    except Exception as e:
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
                engine.save(x)

            removed_ids = d['removed_member_ids']
            for rid in removed_ids:
                engine.query(Member).filter(Member.id == rid).delete()
            return json.dumps({"status": "ok", "message": "saved"})
        elif request.method == 'GET':
            m = engine.query(Member).filter(Member.group_id == group_id).all()
            return json.dumps(m, cls=AlchemyEncoder)
            #return render_template('member/{0}.html'.format('member'))
        else:
            return abort(404)
    except Exception as e:
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
            engine.save(x)

            return json.dumps({"status": "ok", "message": "saved"})
        else:
            return abort(404)
    except Exception as e:
        logging.exception(e)
        return render_template("oops.html")
