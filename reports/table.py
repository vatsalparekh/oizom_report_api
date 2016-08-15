import HTML
import time
import requests
import json


def table_generate():  # takes device_id as a parameter for html_name
    table_header = ['Time <br> ( Hourly )']     # make one for (Daily)
    table = []
    gases = []
    req = requests.get(
        "http:tub.oizom.com/57204fe3e595aa1d0004e170/data/range/hours/OZ_POLLUDRON_006?type=IODA&lte=1466879400&gte=1466793000")
    all_gases = {'p2': 'PM10', 'p3': 'PM1', 'g5': 'O3', 'g4': 'NH3',
                 'g3': 'NO2', 'g1': 'CO2', 'temp': 'Temperature',
                 'g6': 'H2S', 'g7': 'aNO2', 'hum': 'Humidity',
                 'lon': 'longitude', 'g9': 'sCO', 'g8': 'SO2',
                 'p1': 'PM2.5', 't': 'Time', 'lat': 'latitude', 'g2': 'CO'}

    gases_avlb = req.json()[0]['payload']['d'].keys()

    gas_sequence = ['p2', 'p1', 'g3', 'g5', 'g2',
                    'g8', 'g4', 'g1', 'temp', 'hum', 'noise']

    param_units = {'p1': '&#181;g/m3', 'p2': '&#181;g/m3', 'g1': 'ppm',
                   'g7': '&#181;g/m3', 'g9': 'mg/m3', 'g5': '&#181;g/m3',
                   'g8': '&#181;g/m3', 'temp': '&#x2103;', 'hum': '%',
                   'g3': '&#181;g/m3', 'g2': 'mg/m3', 'g4': '&#181;g/m3'}

    for x in gas_sequence:
        if x in gases_avlb:
            gases.append(x)
            gases_avlb.remove(x)

    for x in gases_avlb:
        gases.append(x)

    gases.remove('noise')
    gases.remove('t')

    #=====================Table-Header========================================
    for elements in gases:
        try:
            table_header.append(
                str(all_gases[elements]) + "</br>" + " ( " + param_units[elements] + " )")
        except KeyError:
            table_header.append(str(elements))
    #=====================Table===============================================
    for elements in req.json():
        temp = []

        temp.append(time.ctime(
            int(elements['payload']['d']['t'])))

        for gas in gases:
            if gas != 't':
                temp.append(elements['payload']['d'][gas])

        table.append(temp)

    table = HTML.table(table, header_row=table_header)

    table_name = os.path.join('static', device_id +
                              '_table_' + str(int(time.time())) + '.html')
    f = open(table_name, 'w')
    f.write(table)
    f.close()
    return table_name
