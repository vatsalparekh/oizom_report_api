from djcelery import celery
from html_render import html_generate
from pdf import pdf_generate
from mailer import send_mail


@celery.task
def send_report(user_id, device_id, lte, gte, mail_id):

    html_name = html_generate(user_id, device_id, lte, gte, mail_id)
    pdf_name = pdf_generate(html_name)
    send_mail(pdf_name, mail_id)

    print 'Done!' + user_id
