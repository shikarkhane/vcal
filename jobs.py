# import logging
#
# # Log everything, and send it to stderr.
# logging.basicConfig(filename="error.log",level=logging.INFO,format='%(asctime)s %(message)s')
#
# def remind_invitee_to_register():
#     logging.info('remind_invitee_to_register')
# def notify_admin_missing_invitee():
#     # notify when missing invitees after X days of invite send out
#     logging.info('notify_admin_missing_invitee')
# def notify_admin_all_invitees_aboard():
#     # notify when all invitees have registered
#     logging.info('notify_admin_all_invitees_aboard')
# def remind_parent_children_count_per_term():
#     # on new term, make parent fill up child count
#     logging.info('remind_parent_children_count_per_term')
# def notify_admin_missing_child_count():
#     # notify admin, if parents have missed filling child count
#     # and total filled child count is not matching expected child count
#     # and distribution calc is pending for more than X days
#     logging.info('notify_admin_missing_child_count')
# def calculate_days_per_user_per_term():
#     # for each open term and if all child counts are filled, calc day count
#     logging.info('calculate_days_per_user_per_term')
# def remind_to_fill_term_work():
#     # remind to fill term work after X days of calculation send out
#     # advanced: do tracker image, send reminder on sms if they didnt
#     # see email
#     logging.info('remind_to_fill_term_work')
# def remind_on_summoned():
#     # remind week before utfall and give a calendar event click to add option
#     logging.info('remind_on_summoned')
# def notify_admin_unfilled_days():
#     # notify admin of un-filled days, at least 3 weeks in advance but 7 days after term was opened.
#     logging.info('notify_admin_unfilled_days')
# def notify_admin_if_next_term_missing():
#     # notify admin if current term has 1 month left in it, and next term is missing
#     logging.info('notify_admin_if_next_term_missing')
#
#
# # Take care of some imports
# from datetime import datetime
# from flywheel import Model, Field, Engine
#
# # Set up our data model
# class Tweet(Model):
#     userid = Field(hash_key=True)
#     id = Field(range_key=True)
#     ts = Field(type=datetime, index='ts-index')
#     text = Field()
#
#     def __init__(self, userid, id, ts, text):
#         self.userid = userid
#         self.id = id
#         self.ts = ts
#         self.text = text
#
# # Create an engine and connect to an AWS region
# engine = Engine()
# engine.connect(region='dummy', host='localhost', port=8000,  access_key='dummy', secret_key='dummy', is_secure=False, session = None)
#
# # Register our model with the engine so it can create the Dynamo table
# engine.register(Tweet)
#
# # Create the dynamo table for our registered model
# engine.create_schema()

from app.common.jobs import unbooked_dates

unbooked_dates()