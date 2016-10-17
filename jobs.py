import logging

# Log everything, and send it to stderr.
logging.basicConfig(filename="error.log",level=logging.INFO,format='%(asctime)s %(message)s')

def remind_invitee_to_register():
    logging.info('remind_invitee_to_register')
def notify_admin_missing_invitee():
    # notify when missing invitees after X days of invite send out
    logging.info('notify_admin_missing_invitee')
def remind_parent_children_count_per_term():
    # on new term, make parent fill up child count
    logging.info('remind_parent_children_count_per_term')
def notify_admin_missing_child_count():
    # notify admin, if parents have missed filling child count
    # and distribution calc is pending for more than X days
    logging.info('notify_admin_missing_child_count')
def calculate_days_per_user_per_term():
    # for each open term and if all child counts are filled, calc day count
    logging.info('calculate_days_per_user_per_term')
def remind_to_fill_term_work():
    # remind to fill term work after X days of calculation send out
    # advanced: do tracker image, send reminder on sms if they didnt
    # see email
    logging.info('remind_to_fill_term_work')
def remind_on_summoned():
    # remind every week
    logging.info('remind_to_fill_term_work')