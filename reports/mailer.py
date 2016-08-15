import requests
from logs import *


def send_mail(path, mail_id):

    payload = {}

    payload['apikey'] = 'c01b8dad-4773-4cec-bcd0-8113ce7d0a66'
    payload['from'] = 'support@oizom.com'
    payload['fromName'] = 'Oizom Support'
    payload['replyTo'] = 'tech@oizom.com'
    payload['replyToName'] = 'Tech @ Oizom'
    payload['to'] = ';'.join(ids for ids in mail_id)
#   sending mail to multiple email ids
    payload['subject'] = 'Your Air Quality Report has arrived'
    payload['bodyText'] = 'The Air Quality Report is attached'

    pdf = {'attachmentFiles': open(path, 'rb')}

    try:
        mail_req = requests.post(
            'https://api.elasticemail.com/v2/email/send',
            params=payload,
            files=pdf)
        print mail_req.url
#       sends a request to generate and send mail to mail ids
    except Exception, e:
        logger.exception("%s", str(e))

    if (mail_req.status_code == 200):
        logger.info('Mail Sent! mail_id is %s', mail_id)
        return
