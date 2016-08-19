import requests
from logs import *
from datetime import datetime


def send_mail(path, mail_id, gte, lte, label, report_type):

    payload = {}

    payload['apikey'] = 'c01b8dad-4773-4cec-bcd0-8113ce7d0a66'
    payload['from'] = 'support@oizom.com'
    payload['fromName'] = 'Oizom Support'
    payload['replyTo'] = 'hello@oizom.com'
    payload['replyToName'] = 'Hello@Oizom'
    payload['to'] = mail_id
    payload['subject'] = report_type + ' Air Quality Report for ' + label + \
        ' : ' + \
        datetime.fromtimestamp(time.time()).strftime('%d-%b-%y')
    payload['bodyText'] = '''
    Hey,
    Please find attached ''' + report_type + ''' report for your devices.


    Report Date: ''' + datetime.fromtimestamp(
        time.time()).strftime('%d-%B-%Y') + \
        '''.
    Report Data: ''' + time.ctime(int(gte) + 19800) + \
        ' to ' + time.ctime(int(lte) + 19800) + \
        '''


    Please note:
    If you face any issues you can drop a mail to hello@oizom.com .

    Regards,

    Vrushank Vyas
    Oizom Instruments Private Limited
    '''
    pdf = {'attachmentFiles': open(path, 'rb')}

    try:
        mail_req = requests.post(
            'https://api.elasticemail.com/v2/email/send',
            params=payload,
            files=pdf)
        print mail_req.url

    except Exception, e:
        logger.exception("%s", str(e))

    if (mail_req.status_code == 200):
        if mail_req.json()["success"]:
            logger.info('Mail Sent! mail_id is %s', mail_id)
            return
        else:
            print mail_req.json()
