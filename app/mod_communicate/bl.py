from app.mod_communicate.models import EmailNotify
from app.common.constants import Email
import boto3


# Import the database object from the main app module
from app import engine

class Content:
    def __init__(self, type, metric):
        self.type = type
        self.metric = metric
    def getSubject(self):
        if self.type == Email.TERM_OPEN:
            return '[Fyi - Term Open]: {} term is open'
        if self.type == Email.TERM_EDITED:
            return '[Fyi - Term Edited]: {} term was changed'
        if self.type == Email.BOOKED:
            return '[Fyi - Booked]: {} as {}'
        if self.type == Email.SWITCH_BROADCAST:
            return '[Action needed - Byta dag]'
        if self.type == Email.SWITCH:
            return '[Fyi - Switch Published]: {}'
        if self.type == Email.SWITCHED:
            return '[Fyi - Switch Successful]: Someone pitched in'
        if self.type == Email.UNBOOKED_IN_30_DAYS:
            return '[Action needed]: Unbooked dates in next 30 days'
        if self.type == Email.UPCOMING_7_DAYS:
            return '[Info]: Upcoming vikarie week'
        if self.type == Email.SUMMONED:
            return '[Action needed - Summoned]: On {}'
        if self.type == Email.UPDATE_SHOWUPS:
            return '[Action needed - Showups]: Update showups'


    def getContent(self):
        if self.type == Email.TERM_OPEN:
            return '{} ({}) term is open. ' \
                   'Please sign-up for stand-in days.'
        if self.type == Email.TERM_EDITED:
            return '{} ({}) term was changed by the administrator' \
                   'Please login to check, if you are obligated to standin for more days.'
        if self.type == Email.BOOKED:
            return 'You booked {} as {}'
        if self.type == Email.SWITCH_BROADCAST:
            return 'Family {} needs someone else to take their {} on {}.' \
                   'This date is made available when you will view calendar.'
        if self.type == Email.SWITCH:
            return 'Your request to switch {} as {} has been published.' \
                   'Till another user picks your date, you will own it.'
        if self.type == Email.SWITCHED:
            return 'Your {} on {} was picked by {}.' \
                   'Please check if you need to pick any more dates by logging in.'
        if self.type == Email.UNBOOKED_IN_30_DAYS:
            return 'Unbooked dates in next 30 days.\n'\
                   'Following dates are unbooked - \n\n{}'
        if self.type == Email.UPCOMING_7_DAYS:
            return 'Vikarie families booked for upcoming week\n\n\n{}'
        if self.type == Email.SUMMONED:
            return 'You are being called to work on {}. ' \
                   'Please send email to vikarie@gomorronsol.net to confirm the receipt of this email.'
        if self.type == Email.UPDATE_SHOWUPS:
            return 'Please update the people who worked last week.' \
                    'You can do it under the SHOW-UPS section by highlighting the family who worked.'


class Message:
    def __init__(self, email, type, metric, cc=[]):
        self.ses = boto3.client('ses')
        self.email_from = 'do-not-reply@vikariekalender.se'
        self.email_to = email
        self.type = type
        self.metric = metric
        self.cc = cc

    def send(self):
        c = Content(self.type, self.metric)
        subject = (c.getSubject()).format(*(self.metric))
        body = (c.getContent()).format(*(self.metric))

        r = self.send_email( subject, body)
        e = EmailNotify(self.email_to, self.type)
        engine.save(e)

    def send_email(self, subject, body):
        response = self.ses.send_email(
            Source=self.email_from,
            Destination={
                'ToAddresses': [
                    self.email_to,
                ],
                'CcAddresses': self.cc
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': body
                    }
                }
            }
        )