import os
import subprocess


def pdf_generate(html_name):

    options = {
        'page-size': 'Letter',
        'margin-top': '0.5in',
        'margin-right': '0.5in',
        'margin-bottom': '0.5in',
        'margin-left': '0.5in',
        'encoding': "UTF-8",
    }

    pdf_path = os.path.join('static', 'pdf',
                            html_name.split('/')[1].split(".")[0] + '.pdf')

    url = 'http://localhost:8000/' + html_name

    print html_name
    print pdf_path

    try:
        subprocess.check_call(['wkhtmltopdf', url, pdf_path])
    except Exception:
        return

    return 'static/pdf/' + html_name.split('/')[1].split(".")[0] + '.pdf'
