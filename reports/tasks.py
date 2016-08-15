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
#   generates label and location of the user
    try:
        html_name, img_lst, chart_page, table_page = html_generate(
            user_id, device_id, gte, lte, report_type, label, location, org)
#       obtains html of every page in pdf 
        pdf_list = [html_name]
#       creates list pdf_list and inserts html_name, i.e. first page of pdf
        for x in chart_page:
            pdf_list.append(x)
#       appends graph img pages to the pdf_list
        pdf_list.append(table_page)
#       appends last page to pdf
        pdf_name = pdf_generate(pdf_list, label, report_type)
#       generates pdf of all the html pages using pdf_generate()
        send_mail(pdf_name, mail_id)
#       sends mail to the user
#        delete_static(html_name, pdf_name, send_mail)
#
#        logger.info('Done! label: %s mail_id: %s', label, mail_id)

    except Exception, e:
        logger.exception("%s", str(e))


def delete_static(html_name, img, pdf_name):

    try:
        subprocess.call(['rm', html_name])
        subprocess.call(['rm', 'static/chart_imgs/' + img])
        subprocess.call(['rm', pdf_name])

    except Exception, e:
        logger.exception("%s", str(e))
