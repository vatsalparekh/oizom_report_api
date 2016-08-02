import os
import time

def deleted(pdf_name,html_name):
    try:
        os.system("rm ~/oizom_report_api/"+pdf_name)
        os.system("rm ~/oizom_report_api/"+html_name)
        print("Files sent and deleted!")
    except Exception, e:
        print(str(e))
