import requests
import json
from logs import *
import os
import time


def chart_generate(device_id, gas, gas_name, ti, unit):
    chart_payload = {
        "chart": {
            "type": "area",
            "marginBottom": 50
        },
        "title": {
            "text": gas_name + " ( " + unit + " )",
            "x": -20
        },
        "subtitle": {
            "text": "Source: oizom.com",
            "x": -20
        },
        "xAxis": {
            "title": {
                "text": "Time"
            },
            "type": "datetime"
        },
        "yAxis": {
            "title": {
                "text": "( " + unit + " )"
            },
            "plotLines": [{
                "value": 0,
                "width": 1,
                "color": "#808080"
            }]
        },
        "legend": "false",
        "credits": "disable",

        "series": [{
            "name": gas_name,
            "data": gas,
            "pointStart": ti,
            "pointInterval": 3600 * 1000
        }]}

    data = json.dumps(chart_payload)

    try:
        req = requests.post('http://app.oizom.com:4932/', data=data)

    except Exception, e:
        logger.exception(str(e))
        return 'Error in image generation!'

    if req.status_code == 200:
        img = device_id + '_' + gas_name + '_' + str(int(time.time())) + '.png'
        f = open(os.path.join('static', 'chart_imgs', img), 'wb')
        f.write(req.content)
        f.close()
        return img


def html_pg2(device_id, img_lst):

    stylesheet = '''
    <style>
        p{
        font-size: 24px;
        text-align: center;
        }'''

    chart_page = os.path.join(
        'code', 'oizom', device_id + '_' + str(time.time()) + '.html')

    s ='''
            <p><strong>Hourly Average of Last 24 Hours</strong></p>
            <hr />
        '''

    f = open(chart_page, 'a')

    for img in img_lst:
        s += '''
            <div> 
                <img src = " ''' + img + ''' "> </img>
            </div>
            </br>'''
    f.write(s)
    f.close()
