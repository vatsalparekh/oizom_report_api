import requests
import json
import HTML
from datetime import datetime
import time
import os


def html_generate(user_id, device_id, lte, gte, label, location):

    if lte < gte:
        lte, gte = gte, lte

    payload = {'lte': lte, 'gte': gte}

    try:
        req = requests.get('http://tub.oizom.com/' + user_id +
                           '/data/range/hours/' + device_id, params=payload)

    except Exception, e:
        print str(e)

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

        data = json.dumps(chart_payload)

        try:
            req_img = requests.post('http://app.oizom.com:4932/', data=data)

        except Exception, e:
            print str(e)

        if req_img.status_code == 200:

            img = str(device_id) + '_' + str(int(lte)) + \
                str(int(time.time())) + '.png'
            f = open(os.path.join('static', 'chart_imgs', img), 'wb')
            f.write(req_img.content)
            f.close()

            html_name = os.path.join('static', device_id +
                                     '_' + str(int(time.time())) + '.html')

            f = open(html_name, 'w')

            gas_value_table = '''
            <table class="table table-stripped">
             <tbody>

             <tr class="bold">
             <td class="theme-color">AQI</td>
             <td class="text-center white-font theme-color">PM 10 (ug/m3)</td>
             <td class="text-center white-font theme-color" >PM 2.5(ug/m3)</td>
             <td class="text-center white-font theme-color">NO2 (ug/m3)</td>
             <td class="text-center white-font theme-color">O3 (ug/m3)</td>
             <td class="text-center white-font theme-color">CO (mg/m3)</td>
             <td class="text-center white-font theme-color">SO2 (ug/m3)</td>
             <td class="text-center white-font theme-color">NH3 (ug/m3)</td>
             <td class="text-center white-font theme-color">CO2 (ppm)</td>
             <td class="text-center white-font theme-color">Noise (dB)</td>
             </tr>

             <tr>
             <td class="good">Good (0-50)</td>
             <td class="text-center white-font good" >0-50</td>
             <td class="text-center white-font good">0-30</td>
             <td class="text-center white-font good">0-40</td>
             <td class="text-center white-font good">0-50</td>
             <td class="text-center white-font good">0-1.0</td>
             <td class="text-center white-font good">0-40</td>
             <td class="text-center white-font good">0-200</td>
             <td class="text-center white-font good">0-400</td>
             <td class="text-center white-font good">0-40</td>
             </tr>

             <tr>
             <td class="satisfactory">Satisfactory (51-100)</td>
             <td class="text-center white-font satisfactory">51-100</td>
             <td class="text-center white-font satisfactory">31-60</td>
             <td class="text-center white-font satisfactory">41-80</td>
             <td class="text-center white-font satisfactory">51-100</td>
             <td class="text-center white-font satisfactory">1.1-2.0</td>
             <td class="text-center white-font satisfactory">41-80</td>
             <td class="text-center white-font satisfactory">201-400</td>
             <td class="text-center white-font satisfactory">401-500</td>
             <td class="text-center white-font satisfactory">41-60</td>
             </tr>

             <tr>
             <td class="moderate">Moderate (101-200)</td>
             <td class="text-center white-font moderate" >101-250</td>
             <td class="text-center white-font moderate">61-90</td>
             <td class="text-center white-font moderate">81-180</td>
             <td class="text-center white-font moderate">101-168</td>
             <td class="text-center white-font moderate">2.1-10</td>
             <td class="text-center white-font moderate">81-380</td>
             <td class="text-center white-font moderate">401-800</td>
             <td class="text-center white-font moderate">501-600</td>
             <td class="text-center white-font moderate">61-80</td>
             </tr>

             <tr>
             <td class="poor">Poor (201-300)</td>
             <td class="text-center white-font poor" >251-350</td>
             <td class="text-center white-font poor">91-120</td>
             <td class="text-center white-font poor">181-280</td>
             <td class="text-center white-font poor">169-208</td>
             <td class="text-center white-font poor">10-17</td>
             <td class="text-center white-font poor">381-800</td>
             <td class="text-center white-font poor">801-1200</td>
             <td class="text-center white-font poor">601-700</td>
             <td class="text-center white-font poor">81-100</td>
             </tr>

             <tr>
             <td class="verypoor">Very Poor (301-400)</td>
             <td class="text-center white-font verypoor" >351-430</td>
             <td class="text-center white-font verypoor">121-250</td>
             <td class="text-center white-font verypoor">281-400</td>
             <td class="text-center white-font verypoor">209-748</td>
             <td class="text-center white-font verypoor">17-34</td>
             <td class="text-center white-font verypoor">801-1600</td>
             <td class="text-center white-font verypoor">1200-1800</td>
             <td class="text-center white-font verypoor">701-800</td>
             <td class="text-center white-font verypoor">101-120</td>
             </tr>

             <tr>
             <td class="severe">Severe(401-500)</td>
             <td class="text-center white-font severe" >430+</td>
             <td class="text-center white-font severe">250+</td>
             <td class="text-center white-font severe">400+</td>
             <td class="text-center white-font severe">748+</td>
             <td class="text-center white-font severe">34+</td>
             <td class="text-center white-font severe">1600+</td>
             <td class="text-center white-font severe">1800+</td>
             <td class="text-center white-font severe">800+</td>
             <td class="text-center white-font severe">120+</td>
             </tr>
             </tbody>
             </table> '''

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
					.full-sec{width: 100%; padding: 20px 15px; margin-bottom: 25px;} 
					.grayed{background-color: #f8f8f8 ;} 
					.half-sec{width: 48%;text-align: left;font-size: 18px; color:#1a1a1a ; display: inline-block;} 
					.bold{font-weight: bold;}
                     </style>'''

            font = "<link href='https://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>"

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
			                    <p class="normal"> Time from: <span class="underlined bold">''' + time.ctime(int(lte)) + '''</span></p>
			                </div>			        
			                <div class="time-from">
			                    <p class="normal"> Time to: <span class="underlined bold">''' + time.ctime(int(gte)) + '''</span></p>
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

            return html_name, img
