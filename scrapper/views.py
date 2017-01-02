from .tasks import scrap
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def scrap_request(request, scrap_type):

    if scrap_type == 'CPCB':

        scrap.delay()

        return Response("Created Task!")
