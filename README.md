# oizom_report_api


##Install VirtualEnv (optional)
```sudo apt-get install python-virtualenv```

## Steps to install
1. ```Git clone https://github.com/vatsalparekh/oizom_report_api```
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
POST request to ```/report``` with  following json


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
        "report_type":"1",
     },
     {  
        "device_id":"OZ-1",
        "gte":"1469018206",
        "lte":"1468564595",
        "user_id":"ID-1",
        "mail":"client-1@example.com",
        "report_type":"1",
     }
  ]
}
```

#ToDO
- Jenkins CI/CD
- Optimise
- logging where ```Exception``` and ```print```
- Seprate HTML template for mail
