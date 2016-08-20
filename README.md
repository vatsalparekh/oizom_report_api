# oizom_report_api


##Install VirtualEnv (optional)
```sudo apt-get install python-virtualenv```

## Steps to install
1. ```git clone https://github.com/vatsalparekh/oizom_report_api```
2. ```cd oizom_report_api```
3. ```virtualenv venv```
4. ```source venv/bin/active```
5. ```sudo apt-get install python-pip wkhtmltopdf rabbitmq-server xvfb```
6. ```pip install -r requirements.txt```
7. ```cd modules/HTML.py-0.04 ``` -> ```python setup.py install```


-Apply db Migrations ```python manage.py migrate```

-Start Celery        ```python manage.py celeryd &```

if from ```root``` user then on cli -> ```export C_FORCE_ROOT="true"```

-Run django server by  ```python manage.py runserver &```

(```&``` for running it on background)

Bazinga!!!

## API Guidelines
POST request to ```http://ip-or-domain:port/report``` with  following json


```json
{  
  "reports":
  [  
     {  
        "deviceId":"OZ",
        "gte":"1466706600",
        "lte":"1468564595",
        "userId":"ID",
        "mail":"client@example.com",
        "reportType" : "0",
        "org" : "AMC"
     },
     {  
        "deviceId":"OZ-1",
        "gte":"1469018206",
        "lte":"1468564595",
        "userId":"ID-1",
        "mail":"client-1@example.com",
        "reportType" : "1",
        "org" : "CPCB"
     }
  ]
}
```
0 : Daily Report,

1 : Weekly Report,

2 : Monthly Report

#ToDO
- Jenkins CI/CD
- Optimise
- logging where ```Exception``` and ```print```
- Seprate HTML template for mail
