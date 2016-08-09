import requests
import json
from logs import *
import os
import time


def chart_generate(device_id, gas, gas_name, ti, unit):
    
    chart_payload = {
        "chart": {
            "zoomType": 'x',
            "marginBottom": 50
        },
        "title": {
            "text": gas_name + " ( " + unit + " )"
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
            }
        },
        "legend": {
            "enabled": False
        },
        "plotOptions": {
            "area": {
                "fillColor": {
                    "linearGradient": {
                        "x1": 0,
                        "y1": 0,
                        "x2": 0,
                        "y2": 1
                    },
                    "stops": [[0, "#00a8e0"],
                              [1, "#FFFFFF"]]
                },
                "lineWidth": 1,
                "threshold": None
            }
        },
        "series": [{
            "type": 'area',
            "pointStart": ti,
            "pointInterval": 3600 * 1000,
            "name": gas_name,
            "data": gas,
        }]
    }

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
        'static', 'chart_imgs', device_id + '_' + str(time.time()) + '.html')

    s = '''
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
