from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import json
from reports import tasks
from logs import *


@csrf_exempt
@api_view(['POST'])
def get_all_request(request):

    received_data = json.loads(request.body)

    for items in received_data['reports']:

        logger.info("ITEM: %s", items)

        try:
            tasks.send_report.delay(items['userId'],
                                    items['deviceId'],
                                    items['gte'],
                                    items['lte'],
                                    items['mail'],
                                    items['reportType'],
                                    items['org']
                                    )
            print 'Sent to task!'

        except Exception, e:
            logger.exception("%s", str(e))
            continue

    return Response('Recieved Request', status=200)
