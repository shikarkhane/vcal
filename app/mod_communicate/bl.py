from app.mod_communicate.models import EmailNotify
import boto3


# Import the database object from the main app module
from app import engine

class Content:
    def __init__(self, type, metric):
        self.type = type
        self.metric = metric
    def getSubject(self):
        if self.type == 'TERM_OPEN':
            return '{} term is open'
        if self.type == 'TERM_EDITED':
            return '{} term was changed'
        if self.type == 'BOOKED':
            return 'You booked {} as {}'
        if self.type == 'SWITCH':
            return 'Your switch is published'
        if self.type == 'SWITCHED':
            return 'Someone pitched in for you'

    def getContent(self):
        if self.type == 'TERM_OPEN':
            return '{} term is open. ' \
                   'Please sign-up for stand-in days.'
        if self.type == 'TERM_EDITED':
            return '{} term was changed by the administrator' \
                   'Please login to check, if you are obligated to standin for more days.'
        if self.type == 'BOOKED':
            return 'You booked {} as {}'
        if self.type == 'SWITCH':
            return 'Your request to switch {} as {} has been published.' \
                   'Till another user picks your date, you will own it.'
        if self.type == 'SWITCHED':
            return 'Your {} on {} was picked by someone else.' \
                   'Please check if you need to pick any more dates by logging in.'


class Message:
    def __init__(self, email, type, metric):
        self.ses = boto3.client('ses')
        self.email_from = 'do-not-reply@vikariekalender.se'
        self.email_to = email
        self.type = type
        self.metric = metric

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
                'CcAddresses': []
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