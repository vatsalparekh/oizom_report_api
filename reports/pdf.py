import os
import subprocess
from logs import *

def pdf_generate(html_name, label):

    pdf_path = os.path.join('static', 'pdf', label + '_' +
                            html_name.split('_')[-1].split('.')[0] +
                            '.pdf')

    print html_name
    print pdf_path

    try:
        subprocess.check_call(
            ['xvfb-run', '-a', 'wkhtmltopdf', html_name, pdf_path])

    except Exception, e:
        logger.exception("%s",str(e))
        return

    return pdf_path
