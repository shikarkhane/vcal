from flask import Flask, render_template
import logging

# Log everything, and send it to stderr.
logging.basicConfig(filename="error.log",level=logging.INFO,format='%(asctime)s %(message)s')

app = Flask(__name__)

@app.route("/")
def landing():
    try:
        return render_template('landing.html')
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")

@app.route("/dashboard/<usertype>/")
def dashboard(usertype):
    try:
        return render_template('dashboard.html', usertype = usertype)
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")

@app.route("/template/<template>/")
def anytemplate(template):
    try:
        return render_template('{0}.html'.format(template))
    except Exception, e:
        logging.exception(e)
        return render_template("oops.html")

@app.route("/register/", methods=['POST'])
def register():
    # full name, token, password, is_gmail, creation_date, phone numbers
    return render_template('register.html')
@app.route("/group/<groupname>/register/", methods=['POST'])
def register_via_invite():
    # full name, token, password, is_gmail, creation_date, phone numbers
    return render_template('register.html')
@app.route("/group/<groupname>/", methods=['POST'])
def group(groupname):
    # create a group, group_type, group_owner
    return render_template('register.html')
@app.route("/groups/")
def groups():
    # return all groups user belongs to along with is_admin info
    return render_template('register.html')
@app.route("/term/<termname>/", methods=['GET','POST','DEL'])
def term(termname):
    # groupname, term name, start, end, expected_kids_count, is_open
    # check if group has members not signed up yet, notify admin
    # notify that term is open and force to confirm kid count on login
    # dont let anyone sign-up for dates untill everyone has done kid count as expected kid count
    return render_template('register.html')
@app.route("/terms/")
def terms():
    # return all terms for a <group>
    return render_template('register.html')
@app.route("/invite/")
def invite():
    # invite by emails
    return render_template('register.html')
@app.route("/members/", methods=['GET','POST'])
def members():
    # get all members for a group
    # post removals or additions to a group
    return render_template('register.html')
@app.route("/summon/")
def summon():
    # In <group>, summon X number of people on D date for <half day> with <time notes>
    # Inform stand-in via sms
    # More than stand-in needed, inform all admins in group with list of probable people
    # they can call to.
    return render_template('register.html')
@app.route("/showups/", methods=['GET','POST'])
def showups():
    # who all showed up to work today i.e. usernames which showed up.
    # groupname, showup_username, username_of_confirmer
    return render_template('register.html')
@app.route("/children/", methods=['GET','POST','DEL'])
def children_per_term():
    # parent, term name, children count
    return render_template('register.html')
@app.route("/public_holiday/", methods=['GET','POST'])
def public_holiday():
    # groupname, public holday(s)
    return render_template('register.html')
@app.route("/working_day/", methods=['GET','POST'])
def working_day():
    # groupname, working day, number of heads needed, time in notes
    return render_template('register.html')
@app.route("/choose_day/", methods=['GET','POST'])
def choose_day():
    # dont let anyone sign-up for dates untill everyone has done kid count as expected kid count
    # Show visual overlay on sign-up button, explaining the reason for wait
    # groupname, username, date
    return render_template('register.html')
@app.route("/next_available_day/<count>/workday/<is_workday>/")
def next_available_day(count, is_workday):
    # groupname, username, term
    return render_template('register.html')
@app.route("/term_work_status/")
def term_work_status():
    # groupname, username, term
    return render_template('register.html')


if __name__ == '__main__':
    app.run(host= '127.0.0.1', debug=True, port=4949)