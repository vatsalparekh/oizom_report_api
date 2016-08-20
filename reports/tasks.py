from djcelery import celery
from html_render import html_generate
from pdf import pdf_generate
from mailer import send_mail
import subprocess
from logs import *
import requests


@celery.task
def send_report(user_id, device_id, gte, lte, mail_id, report_type,
                org):

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

        logger.info("HTML: %s, IMG: %s, CHART: %s, TABLE:%s",
                    html_name, img_lst, chart_page, table_page)

#       obtains html of every page in pdf
        pdf_list = [html_name]
#       creates list pdf_list and inserts html_name, i.e. first page of pdf

        for x in chart_page:
            pdf_list.append(x)
#       appends graph img pages to the pdf_list
        pdf_list.append(table_page)

        logger.info("PDF: %s", pdf_list)

        pdf_name = pdf_generate(pdf_list, label, report_type)
#       generates pdf of all the html pages using pdf_generate()

        send_mail(pdf_name, mail_id, gte, lte, label, [
                  'Daily', 'Weekly', 'Monthly'][int(report_type)])
#       sends mail to the user
        delete_static(pdf_list + img_lst + [pdf_name])

        logger.info('Done! label: %s mail_id: %s', label, mail_id)

    except Exception, e:
        logger.exception("%s", str(e))


def delete_static(lst):
    try:
        for elements in lst:
            subprocess.call(['rm', elements])

    except Exception, e:
        logger.exception("%s", str(e))
