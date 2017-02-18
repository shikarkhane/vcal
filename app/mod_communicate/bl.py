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
            return 'The term {0} ({1} till {2}) is open. ' \
                   'Please sign-up for stand-in days.'.format(self.metric)

    def getContent(self):
        if self.type == 'TERM_OPEN':
            return 'The term {0} ({1} till {2}) is open. ' \
                   'Please sign-up for stand-in days.'.format(self.metric)

class Message:
    def __init__(self, email, type, metric):
        self.ses = boto3.client('ses')
        self.email_from = 'do-not-reply@vikariekalender.se'
        self.email_to = email
        self.type = type
        self.metric = metric

    def send(self):
        c = Content(self.type, self.metric)
        subject = c.getSubject()
        body = c.getSubject()

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