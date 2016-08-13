import os
import subprocess
from logs import *
from PyPDF2 import PdfFileMerger, PdfFileReader


def pdf_generate(html_name, label):

    pdf_path = os.path.join('static', 'pdf', label + '_' +
                            html_name[0].split('_')[-1].split('.')[0] +
                            '.pdf')

    pdfs = [os.path.join('static', 'pdf', 'part_' +
                         x.split('_')[-1].split('.')[0] +
                         '.pdf') for x in html_name]

    logger.info("HTML Name: %s PDF Path: %s", html_name, pdf_path)

    try:
        for pages, pdf in zip(html_name, pdfs):
            subprocess.check_call(['wkhtmltopdf', pages, pdf])

    except Exception, e:
        logger.exception("%s", str(e))
        return

    merger = PdfFileMerger()

    for files in pdfs:
        merger.append(PdfFileReader(file(files, 'rb')))

    merger.write(pdf_path)

    return pdf_path
