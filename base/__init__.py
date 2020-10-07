# Import flask and template operators
from flask import Flask
from flask_cors import CORS
from flywheel import Engine

SUPER_ADMIN = 'shikarkhane@gmail.com'
ALL_PARENTS = 'parents@gomorronsol.net'

#dynamodb move
engine = Engine()
#engine.connect(region='dummy', host='localhost', port=8000,  access_key='dummy', secret_key='dummy', is_secure=False, session = None)
engine.connect_to_region('eu-west-1')

def create_app():
    # Define the WSGI application object
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    # Configurations
    app.config.from_object('config')



    # Import a module / component using its blueprint handler variable (mod_group)
    from base.mod_draft.controllers import mod_draft as draft_module
    from base.mod_group.controllers import mod_group as group_module
    from base.mod_member.controllers import mod_member as member_module
    from base.mod_workday.controllers import mod_workday as workday_module
    from base.mod_rule.controllers import mod_rule as rule_module
    from base.mod_term.controllers import mod_term as term_module
    from base.mod_switchday.controllers import mod_switchday as switchday_module
    from base.mod_communicate.controllers import mod_communicate as communication_module

    # Register blueprint(s)
    app.register_blueprint(draft_module)
    app.register_blueprint(member_module)
    app.register_blueprint(group_module)
    app.register_blueprint(workday_module)
    app.register_blueprint(rule_module)
    app.register_blueprint(term_module)
    app.register_blueprint(switchday_module)
    app.register_blueprint(communication_module)
    # base.register_blueprint(xyz_module)
    # ..

    return app


def create_app_for_triggered_event():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    return app


def init_db():
    # Build the database:
    # This will create the database file using SQLAlchemy


    from base.mod_draft.models import PublicHoliday
    from base.mod_group.models import Group
    from base.mod_member.models import Invite, Member, User
    from base.mod_rule.models import Rule
    from base.mod_switchday.models import Switchday
    from base.mod_term.models import Children, Term
    from base.mod_workday.models import StandinDay, Summon, Workday
    from base.mod_communicate.models import EmailNotify


    # Register our model with the engine so it can create the Dynamo table
    engine.register(PublicHoliday, Group, Invite, Member, User, Rule, Switchday, Children, Term, StandinDay,
                    Summon, Workday, EmailNotify)

    # Create the dynamo table for our registered model
    engine.create_schema()


