import requests
import json
import HTML
from datetime import datetime
import time
import os
from logs import *


font = "<link href='https://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>"
jquery_js = 'static/jquery.min.js'
style_tag = '''<style>
                    body{font-family:'Open Sans',sans-serif}
                    table{border-collapse:collapse;margin-top:25px;width: 100%}
                    td,th{padding:6px 10px;font-family:sans-serif}
                    .bold{font-weight:700}
                    .text-center{text-align:center}
                    .white-font{color:#fff}
                    .good{background-color:#6ecc58  }
                    .satisfactory{background-color:#bbcf4c }
                    .moderate{background-color:#eac736  }
                    .poor{background-color:#ed9a2e  }
                    .verypoor{background-color:#e8633a  }
                    .severe{background-color:#d63636 }
                    .theme-color,th{background-color:#00b3bf  }
                    .h1{font-size: 36px;margin-bottom: 8px;margin-top: 0px;}
                    .h4{font-size: 18px; margin-bottom: 10px; margin-top: 0px;}
                    .title-left{float: left;display: inline-block;}
                    .img-right{float: right;display: inline-block;height: 90px}
                    .logo-img{margin-top: 20px;}
                    .full-sec{width:100%;padding:20px 15px;margin-bottom:25px;}
                    .grayed{background-color: #f8f8f8 ;}
                    .half-sec{width: 48%;text-align: left;font-size: 18px;
                                    color:#1a1a1a ; display: inline-block;}
                    .bold{font-weight: bold;}
               </style>'''


def html_generate_daily(user_id, device_id, lte, gte, label, location):

    if lte < gte:
        lte, gte = gte, lte

    payload = {'lte': lte, 'gte': gte}
    #location, label = get_loc_label(user_id,device_id)
    try:
        req = requests.get('http://tub.oizom.com/' + user_id +
                           '/data/range/hours/' + device_id, params=payload)

    except Exception, e:
        logger.exception("%s", str(e))

    if (req.status_code == 200):

        table = []
        table_header = ['Time', 'AQI']

        all_gases = {'p2': 'PM10', 'p3': 'PM1', 'g5': 'O3', 'g4': 'NH3',
                     'g3': 'NO2', 'g1': 'CO2', 'temp': 'Temperature',
                     'g6': 'H2S', 'g7': 'aNO2', 'hum': 'Humidity',
                     'lon': 'longitude', 'g9': 'sCO', 'g8': 'SO2',
                     'p1': 'PM2.5', 't': 'Time', 'lat': 'latitude', 'g2': 'CO'}

        gases_avlb = req.json()[0]['payload']['d'].keys()

        gas_sequence = ['p2', 'p1', 'g3', 'g5', 'g2',
                        'g8', 'g4', 'g1', 'temp', 'hum', 'noise']

        gases = []

        gases_avlb.remove('t')

        for x in gas_sequence:
            if x in gases_avlb:
                gases.append(x)
                gases_avlb.remove(x)

        for x in gases_avlb:
            gases.append(x)

        for elements in gases:

            try:
                table_header.append(str(all_gases[elements]))

            except KeyError:
                table_header.append(str(elements))

        for elements in req.json():

            temp = []
            temp.append(datetime.fromtimestamp(
                int(elements['payload']['d']['t'])).strftime('%c'))
            temp.append(elements['aqi'])

            for gas in gases:

                if gas != 't':
                    temp.append(elements['payload']['d'][gas])
            table.append(temp)

        table = HTML.table(table, header_row=table_header)

        aqi = [x['aqi'] for x in req.json()]
        aqi.reverse()

        ti = (int(gte) * 1000) + 19800000  # UTC to localtime

        chart_payload = {
            "chart": {
                "type": "area",
                "height": "600",
                "marginRight": 130,
                "marginBottom": 25
            },
            "title": {
                "text": "Average AQI",
                "x": -20
            },
            "subtitle": {
                "text": "Source: oizom.com",
                "x": -20
            },
            "xAxis": {
                "title": "Time",
                "type": 'datetime'
            },
            "yAxis": {
                "title": {
                    "text": "AQI "
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
                "name": "aqi",
                "data": aqi,
                "pointStart": ti,
                "pointInterval": 3600 * 1000
            }]}

        # data = json.dumps(chart_payload)

        # try:
        #     req_img = requests.post('http://app.oizom.com:4932/', data=data)

        # except Exception, e:
        #     logger.exception("%s", str(e))

        # if req_img.status_code == 200:

        #     img = str(device_id) + '_' + str(int(lte)) + \
        #         str(int(time.time())) + '.png'
        #     f = open(os.path.join('static', 'chart_imgs', img), 'wb')
        #     f.write(req_img.content)
        #     f.close()

        #     html_name = os.path.join('static', device_id +
        #                              '_' + str(int(time.time())) + '.html')

            f = open(html_name, 'w')

            f.write(str(font) +
                    str(style_tag) +
                    '<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>' +
                    '''
                    <div style="display:block; height:92px;">
                		<div class="title-left">
          	            	<div>
          	        	        <p class="h1"> DAILY AIR-POLLUTION REPORT </p>
			        	    </div>
			                <p class="h4"> Report Created on  -  ''' + datetime.now().strftime('%A, %d/%m/%Y ') + '''</p>
			            </div>
			            <div class="img-right">
			                <img class="logo-img" src="http://www.oizom.com/assets/images/discover-mobile-350x350-53-black.png">
                        </div>
                    </div>

					<div class="full-sec grayed">
			            <div class="half-sec">
			                <div class="time-from">
			                    <p class="normal"> Time from: <span class="underlined bold">''' + time.ctime(int(gte)) + '''</span></p>
			                </div>
			                <div class="time-from">
			                    <p class="normal"> Time to: <span class="underlined bold">''' + time.ctime(int(lte)) + '''</span></p>
			                </div>
			            </div>
			            <div class="half-sec">
			                <div class="time-from">
			                    <p class="normal"> Device Location: <span class="underlined bold">''' + location + '''</span></p>
			                </div>
			                <div class="time-from">
			                    <p class="normal"> Device Name: <span class="underlined bold">''' + label + '''</span></p>
			                </div>
			            </div>
			            	<p class="normal" style="margin:0px;"> Pollutants: <span class="underlined bold">''' + ' '.join(str(x) + ',' for x in table_header[2:])[:-1] + '</span></p></div>' +
                    '<img style="display: block; margin:0 auto;" src="chart_imgs/' + img + '"/>' + str(gas_value_table) + str(table) + '<script src="colorService.js"></script>')
            f.close()
            html_header(user_id, device_id, lte, gte, table_header[2:], get_loc_label(
                user_id, device_id)[0], get_loc_label(user_id, device_id)[1])
            return html_name, img


def avg_list(input_list):
    return sum(input_list) / float(len(input_list))


def chart_generate(payload, device_id, gas):

    data = json.dumps(payload)

    try:
        req = requests.post('http://app.oizom.com:4932/', data=data)

    except Exception, e:
        logger.exception(str(e))
        return 'Error in image generation!'

    if req.static == 200:
        img = device_id + '_' + gas + '_' + str(int(time.time())) + '.png'
        f = open(os.path.join('static', 'chart_imgs', img), 'wb')
        f.write(req.content)
        f.close()
        return img


def get_loc_label(user_id, device_id):

    try:
        rq = requests.get('http://tub.oizom.com/' +
                          user_id + '/devices/' + device_id)
        location = rq.json()[0]['loc']
        label = rq.json()[0]['label']

    except Exception, e:
        logger.exception("%s", str(e))

    return location, label


def html_header(user_id, device_id, lte, gte, gases, location, label):
                    user_id, device_id, lte, gte, gases, location, label = \
                                    user_id, device_id, lte, gte, gases, location, label
    return