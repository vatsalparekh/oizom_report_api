import requests
import json
from datetime import datetime
import time
import os
from logs import *

def weekly_chart_generate(aqi_data, ti):
    days = [datetime.fromtimestamp(int(i)).strftime("%b %d") for i in ti[::-1]]
    chart_payload = {
        "chart": {
            "type": 'column'
        },
        "title": {
            "text": 'Daily AQI Average'
        },
        "xAxis": {
            "title": {
                "text": "Days",
            },
            "type": 'category',
            "categories": days,
        },
        "yAxis": {
            "min": 0,
            "title": {
                "text": '( ' + '&#181;g/m3' + ' )',
                "useHTML": True
            }
        },
        "legend": {
            "enabled": False
        },
        "series": [{
            "data": aqi_data
        }]
    }

    data = json.dumps(chart_payload)

    try:
        req = requests.post('http://app.oizom.com:4932/', data=data)

    except Exception, e:
        logger.exception(str(e))
        return 'Error in image generation!'

    if req.status_code == 200:
        img = str(device_id) + '_AQI_' + \
            str(int(time.time())) + '.png'
        f = open(os.path.join('static', 'chart_imgs', img), 'wb')
        f.write(req.content)
        f.close()
        return img

# if __name__ == '__main__':
#   try:
#       rq = requests.get('http://tub.oizom.com/' + user_id +
#                              '/data/range/hours/' + device_id, params=payload)
#   except Exception, e:
        # print(str(e))

#     aqi_data = [element['aqi'] for element in rq.json()]

#     ti = [element['payload']['d']['t'] for element in rq.json()]
#     weekly_chart_generate(aqi_data, ti)
