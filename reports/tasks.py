from djcelery import celery
from html_render import html_generate
from pdf import pdf_generate
from mailer import send_mail
import subprocess
from logs import *
import requests


@celery.task
def send_report(user_id, device_id, gte, lte, mail_id, report_type,
                org='AMC (Ahmedabad Municipal Corporation)'):

    try:
        req = requests.get('http://tub.oizom.com/' +
                           user_id + '/devices/' + device_id)
    except Exception, e:
        logger.exception('%s', str(e))

    label = req.json()[0]['label']
    location = req.json()[0]['loc']

    try:
        html_name, img_lst, chart_page, table_page = html_generate(
            user_id, device_id, gte, lte, report_type, label, location, org)

        pdf_list = [html_name]
        for x in chart_page:
            pdf_list.append(x)
        pdf_list.append(table_page)
        pdf_name = pdf_generate(pdf_list, label, report_type)

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
