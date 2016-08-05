from djcelery import celery
from html_render import html_generate
from pdf import pdf_generate
from mailer import send_mail
import subprocess
from logs import *


@celery.task
def send_report(user_id, device_id, lte, gte, mail_id, label,
                report_type, location):

    if report_type == '1':

        try:
            html_name, img = html_generate(
                user_id, device_id, lte, gte, label, location)
            pdf_name = pdf_generate(html_name, label)
            send_mail(pdf_name, mail_id)

        except Exception, e:
            print str(e)

    try:
        subprocess.call(['rm', html_name])
        subprocess.call(['rm', 'static/chart_imgs/' + img])
        subprocess.call(['rm', pdf_name])

    except Exception, e:
        logger.exception("%s", str(e))

    logger.info('Done! label: %s mail_id: %s',label, mail_id )
