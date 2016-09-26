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

    #   generates label and location of the user
    try:
        req = requests.get('http://api.oizom.com/' +
                           user_id + '/devices/' + device_id,
                           headers={'air-quality-india-app': 'no-auth'})
        logger.info(req.json())
    except Exception, e:
        logger.exception('%s', str(e))

    label = req.json()[0]['label']
    location = req.json()[0]['loc']

    try:
        html_name, img_lst, chart_page, table_page = html_generate(
            user_id, device_id, gte, lte, report_type, label, location, org)

        logger.info("HTML: %s,\n IMG: %s,\n CHART: %s,\n TABLE:%s",
                    html_name, img_lst, chart_page, table_page)

#   obtains html of every page in pdf

        pdf_list = [html_name]
#   creates list pdf_list and inserts html_name, i.e. first page of pdf

        for x in chart_page:
            pdf_list.append(x)

#   appends graph img pages to the pdf_list
        pdf_list.append(table_page)

        logger.info("PDF: %s", pdf_list)

#   generates pdf of all the html pages using pdf_generate()
        pdf_name, pdfs = pdf_generate(pdf_list, label, report_type)

#   sends mail to mail_id
        send_mail(pdf_name, mail_id, gte, lte, label, [
                  'Daily', 'Weekly', 'Monthly'][int(report_type)])

        img_list = ['static/chart_imgs/' + str(img) for img in img_lst]

        delete_static(pdf_list + img_list + [pdf_name] + pdfs)

        logger.info('Done! label: %s mail_id: %s', label, mail_id)

    except Exception, e:
        logger.exception("%s", str(e))


def delete_static(lst):

    print lst

    try:
        for elements in lst:
            logger.info("ELEMENT: %s", elements)
            subprocess.call(['rm', elements])

    except Exception, e:
        logger.exception("%s", str(e))
