from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import document
import json
from datetime import datetime
from djqscsv import render_to_csv_response
# Create your views here.


@csrf_exempt
@api_view(['POST'])
def csv_update(request):
    data = json.loads(str(request.body).decode('utf-8'))

    try:
        if type(data) == list:

            for items in data:
                doc = document()

                try:
                    doc.deviceId = items['deviceId']
                except Exception:
                    pass

                try:
                    doc.label = items['label']
                except Exception:
                    pass

                try:
                    doc.loc = items['loc']
                except Exception:
                    pass

                try:
                    doc.latitude = items['lat']
                except Exception:
                    pass

                try:
                    doc.longitude = items['long']
                except Exception:
                    pass

                try:
                    doc.t = datetime.fromtimestamp(int(items['t']))
                    print (doc.t)
                except Exception as e:
                    print (e)

                try:
                    doc.AQI = items['aqi']
                except Exception:
                    pass

                try:
                    doc.PM10 = items['pm10']
                except KeyError:
                    try:
                        doc.PM10 = items['p2']
                    except Exception:
                        pass

                try:
                    doc.PM25 = items['pm25']
                except KeyError:
                    try:
                        doc.PM25 = items['p1']
                    except Exception:
                        pass

                try:
                    doc.CO = items['g2']
                except KeyError:
                    try:
                        doc.CO = items['co']
                    except KeyError:
                        pass

                try:
                    doc.O3 = items['g5']
                except KeyError:
                    try:
                        doc.O3 = items['o3']
                    except Exception:
                        pass

                try:
                    doc.SO2 = items['g8']
                except KeyError:
                    try:
                        doc.SO2 = items['so2']
                    except Exception:
                        pass

                try:
                    doc.NO2 = items['g7']
                except KeyError:
                    try:
                        doc.NO2 = items['no2']
                    except KeyError:
                        pass

                try:
                    doc.temp = items['temp']
                except Exception:
                    pass

                try:
                    doc.hum = items['hum']
                except Exception:
                    pass

                try:
                    doc.WD = items['wd']
                except Exception:
                    pass

                try:
                    doc.WS = items['ws']
                except Exception:
                    pass

                try:
                    doc.pressure = items['prs']
                except Exception:
                    pass

                try:
                    doc.rainGaige = items['rg']
                except Exception:
                    pass

                doc.save()
        elif type(data) == dict:
            doc = document()

            try:
                doc.deviceId = data['deviceId']
            except Exception:
                pass

            try:
                doc.label = data['label']
            except Exception:
                pass

            try:
                doc.loc = data['loc']
            except Exception:
                pass

            try:
                doc.latitude = data['lat']
            except Exception:
                pass

            try:
                doc.longitude = data['long']
            except Exception:
                pass

            try:
                doc.t = datetime.fromtimestamp(int(data['t']))
                print (doc.t)
            except Exception as e:
                print (e)

            try:
                doc.AQI = data['aqi']
            except Exception:
                pass

            try:
                doc.PM10 = data['pm10']
            except KeyError:
                try:
                    doc.PM10 = data['p2']
                except Exception:
                    pass

            try:
                doc.PM25 = data['pm25']
            except KeyError:
                try:
                    doc.PM25 = data['p1']
                except Exception:
                    pass

            try:
                doc.CO = data['g2']
            except KeyError:
                try:
                    doc.CO = data['co']
                except KeyError:
                    pass

            try:
                doc.O3 = data['g5']
            except KeyError:
                try:
                    doc.O3 = data['o3']
                except Exception:
                    pass

            try:
                doc.SO2 = data['g8']
            except KeyError:
                try:
                    doc.SO2 = data['so2']
                except Exception:
                    pass

            try:
                doc.NO2 = data['g7']
            except KeyError:
                try:
                    doc.NO2 = data['no2']
                except KeyError:
                    pass

            try:
                doc.temp = data['temp']
            except Exception:
                pass

            try:
                doc.hum = data['hum']
            except Exception:
                pass

            try:
                doc.WD = data['wd']
            except Exception:
                pass

            try:
                doc.WS = data['ws']
            except Exception:
                pass

            try:
                doc.pressure = data['prs']
            except Exception:
                pass

            try:
                doc.rainGaige = data['rg']
            except Exception:
                pass

            doc.save()

        d = {'result': 'Executed!'}

    except Exception as e:
        print e
        d = {'error': str(e)}

    return Response(d)


@api_view(['GET'])
def retrive(request, deviceid, gte, lte):
    try:
        gte_formated = datetime.fromtimestamp(int(gte))
        lte_formated = datetime.fromtimestamp(int(lte))

        doc = document.objects.filter(
            deviceId=deviceid, t__gte=gte_formated, t__lte=lte_formated)
    except Exception as e:
        print e

    return render_to_csv_response(doc, filename=str(deviceid), append_datestamp=True)


@api_view(['GET'])
def retrive_deviceid(request, deviceid):
    try:
        doc = document.objects.filter(deviceId=deviceid)
    except Exception as e:
        print e

    return render_to_csv_response(doc, filename=str(deviceid), append_datestamp=True)
