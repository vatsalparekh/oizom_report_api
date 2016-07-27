import os
import subprocess


def pdf_generate(html_name):

    pdf_path = os.path.join('static', 'pdf',
                            html_name.split('/')[1].split(".")[0] + '.pdf')

    print html_name
    print pdf_path

    try:
        subprocess.check_call(
            ['xvfb-run', '-a', 'wkhtmltopdf', html_name, pdf_path])
    except Exception:
        return

    return 'static/pdf/' + html_name.split('/')[1].split(".")[0] + '.pdf'
