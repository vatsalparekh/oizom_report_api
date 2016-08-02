from djcelery import celery
from html_render import html_generate
from pdf import pdf_generate
from mailer import send_mail
import os

@celery.task
def send_report(user_id, device_id, lte, gte, mail_id, label,
                report_type, location):

    if report_type == '1':

        html_name = html_generate(
            user_id, device_id, lte, gte, label, location)
        pdf_name = pdf_generate(html_name, label)
        send_mail(pdf_name, mail_id)
        os.system("rm ../oizom_report_api/"+pdf_name)
        os.system("rm ../oizom_report_api/"+html_name)
    print 'Done!' + label + mail_id
