# oizom_report_api


##Install VirtualEnv (optional)
```sudo apt-get install python-virtualenv```

## Steps to install
1. ```Git clone https://github.com/vatsalparekh/oizom_report_api```
2. ```cd oizom_report_api```
3. ```virtualenv venv```
4. ```source venv/bin/active```
5. ```pip install -r requirements.txt```
6. ```python modules/HTML.py-0.04/setup.py install```
7. ```sudo apt-get install wkhtmltopdf``` or ```pip install pdfkit```

Bazinga!!!
Run by ```python manage.py runserver```

## API Guidelines
POST request to ```/report/``` with  following json


```json
{  
  "reports": 
  [  
     {  
        "device_id":"OZ",
        "gte":"1466706600",
        "lte":"1468564595",
        "user_id":"ID",
        "mail":"client@example.com"
     },
     {  
        "device_id":"OZ-1",
        "gte":"1469018206",
        "lte":"1468564595",
        "user_id":"ID-1",
        "mail":"client-1@example.com"
     }
  ]
}
```

#ToDO
- Queue mechanism for large number or reports 
- Files deletion after mailing
