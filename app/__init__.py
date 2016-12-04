# Import flask and template operators
from flask import Flask, render_template, g
from flask_babel import Babel
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# translations using flask babel
babel = Babel(app)

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)


@babel.localeselector
def get_locale():
    return g.current_lang

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('oops.html'), 404

# Import a module / component using its blueprint handler variable (mod_group)
from app.mod_draft.controllers import mod_draft as draft_module
from app.mod_group.controllers import mod_group as group_module
from app.mod_member.controllers import mod_member as member_module
from app.mod_workday.controllers import mod_workday as workday_module
from app.mod_rule.controllers import mod_rule as rule_module
from app.mod_term.controllers import mod_term as term_module
from app.mod_switchday.controllers import mod_switchday as switchday_module
from app.mod_actionday.controllers import mod_actionday as actionday_module


# Register blueprint(s)
app.register_blueprint(draft_module)
app.register_blueprint(member_module)
app.register_blueprint(group_module)
app.register_blueprint(workday_module)
app.register_blueprint(rule_module)
app.register_blueprint(term_module)
app.register_blueprint(switchday_module)
app.register_blueprint(actionday_module)

# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy

db.create_all()
with app.app_context():
    g.current_lang = 'en'
