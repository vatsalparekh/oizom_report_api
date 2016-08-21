import os
import subprocess
from logs import *
from PyPDF2 import PdfFileMerger, PdfFileReader
from datetime import datetime


def pdf_generate(html_name, label, report_type):

    name = ['Daily Report', 'Weekly Report',
            'Monthly Report'][int(report_type)]
#   applying formatting according to report type
    if report_type == '0':
        fmt = '%d %b, %y'
    elif report_type == '1':
        fmt = '%b'
    elif report_type == '2':
        fmt = '%B'

#   creates path for the final pdf
    pdf_path = os.path.join('static', 'pdf', name + '_' +
                            label + '_' +
                            html_name[0].split('_')[-1].split('.')[0] + '.pdf')

#   creates path for individual pages of pdf
    pdfs = [os.path.join('static', 'pdf', 'part_' + x.split('/')
                         [1].split('.')[0] + '.pdf') for x in html_name]

#   generates pdf from html part by part
    try:
        for pages, pdf in zip(html_name, pdfs):
            subprocess.check_call(
                ['xvfb-run', '-a', 'wkhtmltopdf', pages, pdf])

    except Exception, e:
        logger.exception("%s", str(e))
        return

    merger = PdfFileMerger()

#   merges all the pdf page formed
    for files in pdfs:
        merger.append(PdfFileReader(file(files, 'rb')))

    merger.write(pdf_path)

    return pdf_path, pdfs
