from djcelery import celery
from html_render import html_generate
from pdf import pdf_generate
from mailer import send_mail
import subprocess
from logs import *
import requests


@celery.task
def send_report(user_id, device_id, gte, lte, mail_id, report_type):

    try:
        req = requests.get('http://tub.oizom.com/' +
                           user_id + '/devices/' + device_id)
    except Exception, e:
        logger.exception('%s', str(e))

    label = req.json()[0]['label']
    location = req.json()[0]['loc']

    try:
        html_name, img_lst, chart_page, table_page = html_generate(
            user_id, device_id, gte, lte, report_type, label, location)
        chart_page = ' '.join(str(x) for x in chart_page)
        pdf_name = pdf_generate([html_name, chart_page, table_page], label)
        send_mail(pdf_name, mail_id)

#        delete_static(html_name, pdf_name, send_mail)
#
#        logger.info('Done! label: %s mail_id: %s', label, mail_id)

    except Exception, e:
        print str(e)


def delete_static(html_name, img, pdf_name):

    try:
        subprocess.call(['rm', html_name])
        subprocess.call(['rm', 'static/chart_imgs/' + img])
        subprocess.call(['rm', pdf_name])

    except Exception, e:
        logger.exception("%s", str(e))
