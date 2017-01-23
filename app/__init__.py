# Import flask and template operators
from flask import Flask, render_template
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flywheel import Engine

#dynamodb move
engine = Engine()
engine.connect(region='dummy', host='localhost', port=8000,  access_key='dummy', secret_key='dummy',
               is_secure=False, session = None)

# Define the WSGI application object
app = Flask(__name__)
CORS(app)

# Configurations
app.config.from_object('config')


# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)


# Import a module / component using its blueprint handler variable (mod_group)
from app.mod_draft.controllers import mod_draft as draft_module
from app.mod_group.controllers import mod_group as group_module
from app.mod_member.controllers import mod_member as member_module
from app.mod_workday.controllers import mod_workday as workday_module
from app.mod_rule.controllers import mod_rule as rule_module
from app.mod_term.controllers import mod_term as term_module
from app.mod_switchday.controllers import mod_switchday as switchday_module


# Register blueprint(s)
app.register_blueprint(draft_module)
app.register_blueprint(member_module)
app.register_blueprint(group_module)
app.register_blueprint(workday_module)
app.register_blueprint(rule_module)
app.register_blueprint(term_module)
app.register_blueprint(switchday_module)

# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy

db.create_all()

from app.mod_group.models import Group
# Register our model with the engine so it can create the Dynamo table
engine.register(Group)
# Create the dynamo table for our registered model

engine.create_schema()

