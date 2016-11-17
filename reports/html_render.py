import requests
import json
import HTML
from datetime import datetime
import time
import os
from logs import *
import math


font = "<link href='https://fonts.googleapis.com/css?family=Open+Sans:400,800italic,800,700italic,700,600italic,600,400italic,300italic,300' rel='stylesheet' type='text/css'>"
jquery_js = '<script src="jquery.min.js"></script>'
style_tag = '''
<style>
body{font-family:'Open Sans',sans-serif}
table{border-collapse:collapse;margin-top:25px;width: 100%}
td,th{
    padding:20px 15px;
    font-family:sans-serif;
    text-align: center;
    font-size: 16px;}
.bold{font-weight:700}
.text-center{text-align:center}
.white-font{color:#fff}
.good{background-color:#6ecc58 }
.satisfactory{background-color:#bbcf4c }
.moderate{background-color:#eac736 }
.poor{background-color:#ed9a2e }
.verypoor{background-color:#e8633a }
.severe{background-color:#d63636 }
.theme-color{background-color:#00b3bf }
.h1{font-size: 36px;margin-bottom: 8px;margin-top: 0px;}
.h4{font-size: 18px; margin-bottom: 10px; margin-top: 0px;}
.title-left{float: left;display: inline-block;}
.img-right{float: right;display: inline-block;height: 90px}
.logo-img{margin-top: 20px;}
.full-sec{width: 100%; padding: 20px 15px;}
.underlined-div{
    background-color: transparent;
    border-top: 1px solid #1a1a1a;
    border-bottom: 1px solid #1a1a1a;}
.half-sec{
    width: 48%;text-align: left;
    font-size: 18px;
    color:#1a1a1a;
    display: inline-block;}
.underlined{text-decoration: underline;color: #000; }
.bold{font-weight: bold;}
.h2{font-size: 28px; margin-top: 8px;}
.title-center{text-align: center;display: block;}
p{margin-bottom: 0px;}
.average-aqi-section{padding: 25px 3em; border-bottom: 1px solid #1a1a1a;}
.average-aqi-section p{margin: 0px; font-size: 32px;font-weight: normal;}
.average-aqi-section span.aqi-answer{
    margin: 0px 30px;
    font-size: 40px;
    width: 200px;
    text-decoration: underline;
    text-align: center;
    font-weight: bold}
.units{font-size: 12px; font-weight: lighter;}
.average td{padding: 25px 15px;}
.average-aqi-section.small p{font-size: 20px;font-weight: normal;}
.average-aqi-section.small span.aqi-answer{
    font-size: 20px;font-weight: bold;}
.text-left{text-align: left;}
.aqi-value{font-size: 18px}
.time-value{font-size: 14px;}
.logo-footer{height: 20px; margin-left:5px; margin-bottom: -3px;}
.display-inline{display: inline}
.margin-top-25{margin-top: 25px;}
.right-float{float: right;}
.text-right{text-align: right;}
.float-left{float: left}
.margin-l-3em{margin-left: 3em}
.margin-r-3em{margin-right: 3em}
.chart-imgs img{margin-right:auto;margin-left: auto;border:1px solid #5d5d5d ;}
.chart-imgs{margin-bottom: 25px;width: 100%;text-align: center;}
.approved-container{
border-bottom: 1px solid #5d5d5d;
 display: block; width: 100%; padding-bottom: 15px; font-size: 14px;}
.approved-blank{width: 59%;display: inline-block;}
.approved-div{ text-align: left; width: 40%;display: inline-block;}
.verified-signature{
    width: 80%;
    margin-top: 5px;
    height: 60px;
    border: 1px solid #5d5d5d;
}
</style>
'''


def html_generate(user_id, device_id, gte, lte, report_type, label,
                  location, org):

    report_type = str(report_type)
    payload = {'lte': lte, 'gte': gte}

    lte = int(float(lte))
    gte = int(float(gte))

    lte += 19800
    gte += 19800

    if report_type == '0':

        try:
            req = requests.get('http://api.oizom.com/' + user_id +
                               '/data/hours/24/' + device_id,
                               headers={'air-quality-india-app': 'no-auth'})
            print req.url
            print req.json()
            logger.info(req.json())

        except Exception, e:
            logger.exception("%s", str(e))

        if req.status_code == 200:

            overview_page, img_lst, chart_page, table_page = generate_overview(
                req, report_type, gte, lte, label, location, org, device_id)

            return overview_page, img_lst, chart_page, table_page

    elif report_type == '1' or '2':
        # @Jim
        try:
            req = requests.get('http://api.oizom.com/' + user_id +
                               '/data/days/7' + device_id,
                               params=payload,
                               headers={'air-quality-india-app': 'no-auth'})
            print req.url
            print req.json()
            logger.info(req.json())

        except Exception, e:
            logger.exception("%s", str(e))

        if req.status_code == 200:

            overview_page, img_lst, chart_page, table_page = generate_overview(
                req, report_type, gte, lte, label, location, org, device_id)

            return overview_page, img_lst, chart_page, table_page


def generate_overview(req, report_type, gte, lte, label,
                      location, org, device_id):

    correction_factor = {
        # 'p1': 2,
        # 'p2': 2,
        # 'g5': 0.162,
        # 'g6': 0.00134,
        # 'g7': 1.87,
        # 'g8': 0.52,
        't': 19800
    }
    #
    temp = req.json()
    req = []
    try:
        for elements in temp:
            for keys in correction_factor.keys():

                if keys == 't':
                    elements['payload']['d'][keys] = int(
                        elements['payload']['d'][keys]) + \
                        correction_factor[keys]

                else:
                    try:
                        elements['payload']['d'][keys] = round(float(
                            elements['payload']['d'][keys]), 2) * correction_factor[keys]
                    except KeyError:
                        continue

    except Exception, e:
        print str(e)

    req = temp

    gas_avlb = req[0]['payload']['d'].keys()

    all_gases = {'p2': 'PM10', 'p3': 'PM1', 'g5': 'O3', 'g4': 'NH3',
                 'g3': 'NO2', 'g1': 'CO2', 'temp': 'Temperature',
                 'g6': 'CO', 'g7': 'NO2', 'hum': 'Humidity',
                 'lon': 'longitude', 'g9': 'CO', 'g8': 'SO2', 'noise': 'Noise',
                 'p1': 'PM2.5', 't': 'Time', 'lat': 'latitude', 'g2': 'CO'}

    gas_sequence = ['p2', 'p1', 'g7', 'g5',
                    'g6', 'g8', 'g1', 'temp', 'hum', 'noise']

    param_units = {'p1': '&#181;g/m3', 'p2': '&#181;g/m3', 'g1': 'ppm',
                   'g7': '&#181;g/m3', 'g9': 'mg/m3', 'g5': '&#181;g/m3',
                   'g8': '&#181;g/m3', 'temp': '&#x2103;', 'hum': '%',
                   'g3': '&#181;g/m3', 'g2': 'mg/m3', 'g4': '&#181;g/m3',
                   'g6': 'mg/m3'}

    name = ['Daily', 'Weekly', 'Monthly'][int(report_type)]

    gases = []

    for gas in gas_sequence:
        if gas in gas_avlb:
            gases.append(gas)

    only_gases = [x for x in gases if x not in ['temp', 'hum', 'noise']]

    if report_type == '0':
        pages = str(2 + int(math.ceil(len(only_gases) / 3.0)))
    else:
        pages = '3'

    avg_aqi = round(avg_list([round(float(x['aqi']), 2) for x in req]), 2)

    avg_gas = []
    min_gas = []
    max_gas = []
    min_gas_timestamp = []
    max_gas_timestamp = []

    img_lst = []

    for gas in only_gases:

        all_values = [(round(float(x['payload']['d'][gas]), 2),
                       int(x['payload']['d']['t']))
                      for x in req]

        if report_type == '0':
            img_lst.append(chart_generate(
                device_id, [x[0] for x in all_values], all_gases[gas],
                gte, param_units[gas], report_type))

        avg_gas.append(round(avg_list([x[0] for x in all_values]), 2))

        max_gas.append(round(float(max(all_values)[0]), 2))
        max_gas_timestamp.append((
            datetime.fromtimestamp(
                max(all_values)[1] - 3600).strftime('%H:%M') +
            '-' + datetime.fromtimestamp(
                max(all_values)[1]).strftime('%H:%M'),
            datetime.fromtimestamp(max(all_values)[1])
            .strftime('%b %d, \'%y')))

        min_gas.append(round(float(min(all_values)[0]), 2))
        min_gas_timestamp.append((
            datetime.fromtimestamp(
                min(all_values)[1] - 3600).strftime('%H:%M') +
            '-' + datetime.fromtimestamp(
                min(all_values)[1]).strftime('%H:%M'),
            datetime.fromtimestamp(min(all_values)[1])
            .strftime('%b %d, \'%y')))

    try:
        avg_tempr = str(round(float(avg_list([x['payload']['d']['temp']
                                              for x in req])), 2)) + '&#x2103;'
    except KeyError:
        avg_tempr = 'Not Found'

    try:
        avg_hum = str(round(float(avg_list([x['payload']['d']['hum']
                                            for x in req])), 2)) + '%'
    except KeyError:
        avg_hum = 'Not Found'

    table = [['Average'] + avg_gas] + \
        [['Maximum'] + max_gas] + \
        [[''] + [x[0] for x in max_gas_timestamp]] + \
        [[''] + [x[1] for x in max_gas_timestamp]] + \
        [['Minimum'] + min_gas] + \
        [[''] + [x[0] for x in min_gas_timestamp]] + \
        [[''] + [x[1] for x in min_gas_timestamp]]

    html_code = ''
    header = html_header(
        org, name, lte, gte, gases, label, location)

    html_code = font + jquery_js + style_tag + header + \
        '''<div class="average-aqi-section">
            <p> Average AQI (24 hours):
            <span class="aqi-answer">&nbsp;&nbsp;&nbsp;''' + \
        str(avg_aqi) + '&nbsp;&nbsp;&nbsp;</span></p></div><br>' + \
        '<p style="font-size:16px"> <strong>Daily Overview (24 hours)</strong> <br>' + \
        HTML.table(table, header_row=[''] + [all_gases[x] + '<br>(' + param_units[x] + ')' for x in only_gases]) + \
        '''<div class="average-aqi-section small">
        <p> Average Temperature:
        <span class="aqi-answer">&nbsp;&nbsp;&nbsp;''' + \
        avg_tempr + '&nbsp;&nbsp;&nbsp;</span></p><br>' + \
        '''<p> Average Humidity:
        <span class="aqi-answer">&nbsp;&nbsp;&nbsp;''' + \
        avg_hum + '&nbsp;&nbsp;&nbsp;</span></p><br></div>' + \
        '''<div class="approved-container">
        <div class="approved-blank">
        &nbsp;
        </div>
        <div class="approved-div">
            <p> Verified by: </p>
        <div class="verified-signature">
        </div>
            <p> Name : ________________________________________</p>
            <p> Date &nbsp;&nbsp;: ________________________________________</p>
            <p> Place&nbsp;&nbsp;: ________________________________________</p>
        </div>
        </div>''' + \
        '''<div class="float-left margin-top-25 margin-l-3em display-inline">
        Page 1 out of ''' + pages + \
        '''</div>
        <div class="display-inline margin-r-3em right-float text-right margin-top-25">
        Powered by <img src="black-logo.png" class="logo-footer">
        </div>'''

    html_name = 'static/' + device_id + '_overview_' + \
        str(int(time.time())) + '.html'

    f = open(html_name, 'w')
    f.write(html_code)
    f.close()

    if report_type == '0':
        chart_page = generate_gas_charts(device_id, img_lst, header,
                                         report_type, pages)
        table_page = generate_table(req, device_id, header, report_type, pages)

        return html_name, img_lst, chart_page, table_page

    elif report_type == '1' or '2':
        temp_gas_data = [x['aqi'] for x in req]
        temp_gas_time = [int(x['payload']['d']['t']) for x in req]

        chart = chart_generate(
            device_id, temp_gas_data, 'AQI', temp_gas_time,
            'Ug/m3', report_type)
        img_lst.append(chart)

        chart_page = generate_gas_charts(
            device_id, img_lst, header, report_type, pages)
        table_page = generate_table(req, device_id, header, report_type, pages)

        return html_name, img_lst, chart_page, table_page


def generate_gas_charts(device_id, img_lst, header, report_type, pages):

    chart_list = []

    for l in range(int(math.ceil(len(img_lst) / 3.0))):

        chart_page = os.path.join(
            'static', str(device_id) + '_chart_' +
            str(int(time.time())) + '_' + str(l) + '.html')

        f = open(chart_page, 'w')

        s = font + style_tag + header

        if report_type == '0':
            s += ''' <p style="font-size:16px"><strong>
                Hourly Average of 24 Hours
                </strong></p>
                <br>'''
        if report_type == '1':
            s += ''' <p style="font-size:16px"><strong>
                Daily AQI Average
                </strong></p>
                <br>'''

        for img in img_lst[l * 3:(l + 1) * 3]:

            s += '''
                <div class="chart-imgs">
                    <img src = " ''' + 'chart_imgs/' + str(img) + ''' "> </img>
                </div>
                '''

        s += '''<div class="float-left margin-top-25 margin-l-3em display-inline">
                Page &nbsp;''' + str(l + 2) + ' out of ' + \
            pages + \
            '''</div>
            <div class="display-inline margin-r-3em right-float text-right margin-top-25">
                   Powered by
                   <img src="black-logo.png" class="logo-footer">
               </div>'''

        f.write(s)
        f.close()
        chart_list.append(chart_page)

    return chart_list


def generate_table(req, device_id, header, request_type, pages):

    table_css = '''
    <style>
        table td{padding: 5px 15px;}
        table tr td:first-child{width:20%}
    </style>
    '''
    gas_avlb = req[0]['payload']['d'].keys()

    all_gases = {'p2': 'PM10', 'p3': 'PM1', 'g5': 'O3', 'g4': 'NH3',
                 'g3': 'NO2', 'g1': 'CO2', 'temp': 'Temp.',
                 'g6': 'CO', 'g7': 'NO2', 'hum': 'Hum.',
                 'lon': 'longitude', 'g9': 'CO', 'g8': 'SO2', 'noise': 'Noise',
                 'p1': 'PM2.5', 't': 'Time', 'lat': 'latitude', 'g2': 'CO'}

    gas_sequence = ['p2', 'p1', 'g7', 'g5',
                    'g6', 'g8', 'g1', 'temp', 'hum']

    param_units = {'p1': '&#181;g/m3', 'p2': '&#181;g/m3', 'g1': 'ppm',
                   'g7': '&#181;g/m3', 'g9': 'mg/m3', 'g5': '&#181;g/m3',
                   'g8': '&#181;g/m3', 'temp': '&#x2103;', 'hum': '%',
                   'g3': '&#181;g/m3', 'g2': 'mg/m3', 'g4': '&#181;g/m3',
                   'g6': 'mg/m3'}

    table = []
    gases = []

    for x in gas_sequence:
        if x in gas_avlb:
            gases.append(x)

    table_header = ['Time']

#   =================Table-Header==================
    for elements in gases:
        try:
            table_header.append(
                str(all_gases[elements]) +
                '<br><p style="font-size:12px">(' + str(param_units[elements]) + ')</p>')
        except KeyError:
            table_header.append(str(elements))

#   =====================Table=====================
    for elements in req:
        temp = []

        temp.append(datetime.fromtimestamp(
            int(elements['payload']['d']['t'])).strftime('%H:%M %b %d, \'%y'))

        for gas in gases:
            if gas != 't':
                if(round(float(elements['payload']['d'][gas]), 2) == 0):
                    temp.append("0.0")
                else:
                    temp.append(round(float(elements['payload']['d'][gas]), 2))

        table.append(temp)

    t = HTML.table(table, header_row=table_header,
                   col_width=['30px'] + ['15px' for x in table_header[:-1]],
                   col_align=['center' for x in table_header])

    table_name = os.path.join('static', device_id +
                              '_table_' + str(int(time.time())) + '.html')

    s = style_tag + table_css + jquery_js + header

    if request_type == '0':
        s += '<p style="font-size:16px">Hourly Average of Last 24 Hours</p>'
    else:
        s += '<p style="font-size:16px">Daily Average </p>'

    s += t + '<script src="colorService.js"></script>' + \
        '''<div class="float-left margin-top-25 margin-l-3em display-inline">
        Page ''' + pages + ' out of ' + pages + \
        '''</div>
        <div class="display-inline margin-r-3em right-float text-right margin-top-25">
        Powered by <img src="black-logo.png" class="logo-footer">
        </div>'''

    f = open(table_name, 'w')
    f.write(s)
    f.close()
    return table_name


def html_header(org, name, lte, gte, gases, label, location):

    all_gases = {'p2': 'PM10', 'p3': 'PM1', 'g5': 'O3', 'g4': 'NH3',
                 'g3': 'NO2', 'g1': 'CO2', 'temp': 'Temperature',
                 'g6': 'H2S', 'g7': 'NO2', 'hum': 'Humidity',
                 'lon': 'longitude', 'g9': 'CO', 'g8': 'SO2', 'noise': 'Noise',
                 'p1': 'PM2.5', 't': 'Time', 'lat': 'latitude', 'g2': 'CO'}

    html = '''<div style="display:block; height:92px;">
                <div class="title-center">
                    <div>
                        <p class="h1 bold">''' + org + ''' </p>
                        <p class="h2">''' + name + ''' AIR-POLLUTION REPORT </p>
                    </div>
                </div>
              </div>

              <div class="full-sec underlined-div">
                <div class="half-sec">
                    <div class="time-from">
                        <p class="normal"> Time from: <span class="underlined bold">''' + datetime.fromtimestamp(int(gte)).strftime('%H:%m, %a %d-%m-%Y') + '''</span></p>
                    </div>
                    <div class="time-from">
                        <p class="normal"> Time to: <span class="underlined bold">''' + datetime.fromtimestamp(int(lte)).strftime('%H:%m, %a %d-%m-%Y') + '''</span></p>
                    </div>
                </div>
                <div class="half-sec">
                <div class="time-from">
                    <p class="normal"> Device Name: <span class="underlined bold">''' + label + '''</span></p>
                </div>
                <div class="time-from">
                        <p class="normal"> Device Location: <span class="underlined bold">''' + location + '''</span></p>
                </div>
              </div>
                <p class="normal">
                Pollutants: <span class="underlined bold">''' + \
        (' '.join(str(all_gases[x]) + ',' for x in gases))[:-1] + \
        '</span></p></div>'
    return html


def chart_generate(device_id, gas, gas_name, gte, unit, report_type):

    if report_type == '0':
        chart_payload = {
            "chart": {
                "type": "area",
                "marginBottom": 50
            },
            "title": {
                "text": gas_name + " ( " + unit + " )",
                "x": -20,
                "useHTML": True
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
                    "text": "( " + unit + " )",
                    "useHTML": True
                }
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

            "legend": False,
            "credits": {"enabled": False},

            "series": [{
                "name": gas_name,
                "data": gas,
                "pointStart": (int(gte) * 1000) + 19800000,
                "pointInterval": 3600 * 1000
            }]}

    elif report_type == '1' or '2':
        days = [datetime.fromtimestamp(
            int(x)).strftime("%b %d") for x in gte[::-1]]
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
            "plotOptions": {
                "column": {
                    "pointPadding": -0.2,
                    "borderWidth": 0
                }
            },
            "legend": {
                "enabled": False
            },
            "series": [{
                "data": gas
            }]
        }

    data = json.dumps(chart_payload)

    try:
        req = requests.post('http://localhost:4932/', data=data)

    except Exception, e:
        logger.exception(str(e))
        return 'Error in image generation!'

    if req.status_code == 200:
        img = device_id + '_' + gas_name + '_' + str(int(time.time())) + '.png'
        f = open(os.path.join('static', 'chart_imgs', img), 'wb')
        f.write(req.content)
        f.close()
        return img


def avg_list(input_list):
    return sum(input_list) / len(input_list)
