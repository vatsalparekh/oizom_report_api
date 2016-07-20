from rest_framework.decorators import api_view
import requests
import HTML
import datetime
import json
import time
import os
import pdfkit
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import subprocess


@csrf_exempt
@api_view(['POST'])
def get_all_request(request):

    received_data = json.loads(request.body)
    response = []
    try:
        for items in received_data['reports']:
            response.append([items['mail'], generate(items['user_id'],
                                                     items['device_id'],
                                                     items['lte'],
                                                     items['gte'],
                                                     items['mail']
                                                     )])
    except Exception:
        pass

    return Response(response)


def generate(user_id, device_id, lte, gte, mail=None):

    if lte < gte:
        lte, gte = gte, lte

    payload = {'lte': lte, 'gte': gte}

    try:
        req = requests.get('http://tub.oizom.com/' + user_id +
                           '/data/range/hours/' + device_id, params=payload)
    except Exception:
        pass

    if (req.status_code == 200):

        table = []
        table_header = ['Time', 'AQI']

        all_gases = {'p2': 'PM10', 'p3': 'PM1', 'g5': 'O3', 'g4': 'NH3',
                     'g3': 'NO2', 'g1': 'CO2', 'temp': 'Temperature',
                     'g6': 'H2S', 'g7': 'aNO2', 'hum': 'Humidity',
                     'lon': 'longitude', 'g9': 'sCO', 'g8': 'SO2',
                     'p1': 'PM2.5', 't': 'Time', 'lat': 'latitude', 'g2': 'CO'}

        gases = req.json()[0]['payload']['d'].keys()

        for elements in gases:
            try:
                if elements != 't':
                    table_header.append(str(all_gases[elements]))
            except KeyError:
                table_header.append(str(elements))

        for elements in req.json():
            temp = []
            temp.append(datetime.datetime.fromtimestamp(
                int(elements['payload']['d']['t'])).strftime('%c'))
            temp.append(elements['aqi'])
            for gas in gases:
                if gas != 't':
                    temp.append(elements['payload']['d'][gas])
            table.append(temp)

        table = HTML.table(table, header_row=table_header,
                           border='0',
                           style='''font - family: sans - serif
                           font - color: #ffffff
                           width: 100 %
                           align: center''',
                           col_align=['center' for x in table_header],)

        aqi = [x['aqi'] for x in req.json()]
        aqi.reverse()
        ti = (int(gte) * 1000) + 19800000  # UTC to localtime

        payload = {
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

        data = json.dumps(payload)

        req_img = requests.post('http://app.oizom.com:4932/', data=data)

        if req_img.status_code == 200:

            img = str(device_id) + '_' + str(int(lte)) + \
                str(int(time.time())) + '.png'
            f = open(os.path.join('static', 'chart_imgs', img), 'wb')
            f.write(req_img.content)
            f.close()

            html_name = os.path.join('static', device_id +
                                     '_' + str(int(time.time())) + '.html')

            f = open(html_name, 'w')

            value_table = '''
            <table class="table table-stripped"> <tbody> <tr class="bold"> <td class="theme-color">AQI</td><td class="text-center white-font theme-color">PM 10 (ug/m3)</td><td class="text-center white-font theme-color" >PM 2.5(ug/m3)</td><td class="text-center white-font theme-color">NO2 (ug/m3)</td><td class="text-center white-font theme-color">O3 (ug/m3)</td><td class="text-center white-font theme-color">CO (mg/m3)</td><td class="text-center white-font theme-color">SO2 (ug/m3)</td><td class="text-center white-font theme-color">NH3 (ug/m3)</td><td class="text-center white-font theme-color">CO2 (ppm)</td><td class="text-center white-font theme-color">Noise (dB)</td></tr><tr> <td class="good">Good (0-50)</td><td class="text-center white-font good" >0-50</td><td class="text-center white-font good">0-30</td><td class="text-center white-font good">0-40</td><td class="text-center white-font good">0-50</td><td class="text-center white-font good">0-1.0</td><td class="text-center white-font good">0-40</td><td class="text-center white-font good">0-200</td><td class="text-center white-font good">0-400</td><td class="text-center white-font good">0-40</td></tr><tr> <td class="satisfactory">Satisfactory (51-100)</td><td class="text-center white-font satisfactory">51-100</td><td class="text-center white-font satisfactory">31-60</td><td class="text-center white-font satisfactory">41-80</td><td class="text-center white-font satisfactory">51-100</td><td class="text-center white-font satisfactory">1.1-2.0</td><td class="text-center white-font satisfactory">41-80</td><td class="text-center white-font satisfactory">201-400</td><td class="text-center white-font satisfactory">401-500</td><td class="text-center white-font satisfactory">41-60</td></tr><tr> <td class="moderate">Moderate (101-200)</td><td class="text-center white-font moderate" >101-250</td><td class="text-center white-font moderate">61-90</td><td class="text-center white-font moderate">81-180</td><td class="text-center white-font moderate">101-168</td><td class="text-center white-font moderate">2.1-10</td><td class="text-center white-font moderate">81-380</td><td class="text-center white-font moderate">401-800</td><td class="text-center white-font moderate">501-600</td><td class="text-center white-font moderate">61-80</td></tr><tr> <td class="poor">Poor (201-300)</td><td class="text-center white-font poor" >251-350</td><td class="text-center white-font poor">91-120</td><td class="text-center white-font poor">181-280</td><td class="text-center white-font poor">169-208</td><td class="text-center white-font poor">10-17</td><td class="text-center white-font poor">381-800</td><td class="text-center white-font poor">801-1200</td><td class="text-center white-font poor">601-700</td><td class="text-center white-font poor">81-100</td></tr><tr> <td class="verypoor">Very Poor (301-400)</td><td class="text-center white-font verypoor" >351-430</td><td class="text-center white-font verypoor">121-250</td><td class="text-center white-font verypoor">281-400</td><td class="text-center white-font verypoor">209-748</td><td class="text-center white-font verypoor">17-34</td><td class="text-center white-font verypoor">801-1600</td><td class="text-center white-font verypoor">1200-1800</td><td class="text-center white-font verypoor">701-800</td><td class="text-center white-font verypoor">101-120</td></tr><tr> <td class="severe">Severe(401-500)</td><td class="text-center white-font severe" >430+</td><td class="text-center white-font severe">250+</td><td class="text-center white-font severe">400+</td><td class="text-center white-font severe">748+</td><td class="text-center white-font severe">34+</td><td class="text-center white-font severe">1600+</td><td class="text-center white-font severe">1800+</td><td class="text-center white-font severe">800+</td><td class="text-center white-font severe">120+</td></tr></tbody> </table> '''

            f.write("<link href='https://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>" +
                    "<style> body{font-family:'Open Sans',sans-serif}table{border-collapse:collapse;margin-top:25px}td,th{padding:6px 10px;font-family:sans-serif}.bold{font-weight:700}.text-center{text-align:center}.white-font{color:#fff}.good{background-color:#6ecc58 }.satisfactory{background-color:#bbcf4c }.moderate{background-color:#eac736 }.poor{background-color:#ed9a2e }.verypoor{background-color:#e8633a }.severe{background-color:#d63636 }.theme-color,th{background-color:#00b3bf }</style>" +
                    '<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>' +
                    '<p> Air Quality Report </p>' + '<img src="' + 'chart_imgs/' + img + '" />' + value_table + table + '<script src="colorService.js">' + "</script>")
            f.close()

        res = {'html': html_name}

        return pdf_generate(res, html_name)


def pdf_generate(path, html_name):

    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None,
    }

    path = str(path['html'])
    pdfkit.from_file(path, 'static/pdf/' + html_name.split('/')
                     [1].split(".")[0] + '.pdf',
                     options=options)

    return 'static/pdf/' + html_name.split('/')[1].split(".")[0] + '.pdf'
