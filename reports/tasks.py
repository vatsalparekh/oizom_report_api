from djcelery import celery
from html_render import html_generate
from pdf import pdf_generate
WKHTMLTOPDF_PATH = '/usr/local/bin/wkhtmltopdf'


@celery.task
def send_report(user_id, device_id, lte, gte, mail):

    pdf_generate(html_generate(user_id, device_id, lte, gte, mail))

    print 'Done!' + user_id
