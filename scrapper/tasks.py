from djcelery import celery
from bs4 import BeautifulSoup
import urllib2
import json
import requests
from datetime import datetime
import pyowm

owm = pyowm.OWM('209bc287aba4992c9c58972e2dbf5114')


URL_CPCB = "http://api.airpollution.online/v1/all/public/cpcb"


@celery.task
def scrap():

    all_data = requests.get(URL_CPCB).json()

    for each in all_data:
        try:
            _url = each['url']
            _deviceId = each['deviceId']
            _type = each['type']
            _lat = each['latitude']
            _long = each['longitude']
            _label = each['label']
            _loc = each['loc']
        except:
            pass

        do_scrap.delay(_url, _deviceId, _type, _lat, _long, _label, _loc)


@celery.task
def do_scrap(url, d_id, d_type, lat, lon, label, loc):

    TEMP_JSON = {
        "deviceId": d_id,
        "deviceType": d_type,
        "lat": lat,
        "long": lon,
        "label": label,
        "loc": loc,
        "payload": {
            "d": {}
        },
    }

    # print "Getting data for : " + url
    # print "*"*10

    try:
        URL = url
        req = urllib2.urlopen(URL).read()
        soup = BeautifulSoup(req, "html.parser")

        table = soup.find('table', {'id': 'tblMain'})

        a = table.find_all('table')[3].find_all('tr')[5]
        b = a.find_all('tr')[1::]

        for each in b:
            each_record = each.find_all('td')
            comp_name = (each_record[0].text).lower()

            try:
                date = each_record[1].text
            except:
                pass

            try:
                time = each_record[2].text
            except:
                pass

            # Timestamp creator
            date_new = date.split('/')
            time_new = time.split(':')
            dt = datetime(int(date_new[2]), int(date_new[1]), int(
                date_new[0]), int(time_new[0]), int(time_new[1]))
            timestamp = (dt - datetime(1970, 1, 1)
                         ).total_seconds() - 19800
            TEMP_JSON['payload']['d']['t'] = str(int(timestamp))

            comp_name_ours = ""

            try:
                comp_value = each_record[3].text
            except IndexError:
                pass

            if '*' not in comp_name:
                if comp_name == "pm2.5" or comp_name == "pm2" or comp_name == "pm 2" or comp_name == "pm 2.5":
                    comp_name_ours = "pm25"
                elif comp_name == "pm10":
                    comp_name_ours = "pm10"
                elif comp_name == "o3" or comp_name == "ozone":
                    comp_name_ours = "o3"
                elif comp_name == "so2" or comp_name == "sulphur dioxide" or comp_name == "sulfur dioxide":
                    comp_name_ours = "so2"
                elif comp_name == "co" or comp_name == "carbon monoxide":
                    comp_name_ours = "co"

                elif comp_name == "no2" or comp_name == "nitrogen dioxide":
                    comp_name_ours = "no2"
                elif comp_name == "temperature" or comp_name == "Rack Temperature" or comp_name == "Ambient Temperature":
                    comp_name_ours = "temp"
                elif comp_name == "relative humidity" or comp_name == "humidity" or comp_name == "HUM" or comp_name == "Relative Humidity":
                    comp_name_ours = "hum"

                if len(comp_name_ours) != 0:
                    if comp_value != "NA":
                        TEMP_JSON['payload']['d'][
                            comp_name_ours] = float(comp_value)

        try:
            observation = owm.weather_at_coords(lat, lon)
            w = observation.get_weather()
            TEMP_JSON['payload']['d']['wd'] = w.get_wind()['deg']
            TEMP_JSON['payload']['d']['ws'] = w.get_wind()['speed']
            TEMP_JSON['payload']['d']['temp'] = w.get_temperature('celsius')[
                'temp']
            TEMP_JSON['payload']['d']['hum'] = w.get_humidity()
        except:
            pass
        # print json.dumps(TEMP_JSON)
        headers = {'content-type': 'application/json'}
        response = requests.request(
            "POST", "http://api.airpollution.online/v1/public/data/collection", data=json.dumps(TEMP_JSON), headers=headers)
        # print response.text
        # print "+"*40
    except:
        pass
