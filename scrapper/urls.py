from django.conf.urls import url
from .views import scrap_request

urlpatterns = [
    url(r'^org/(?P<scrap_type>\w+)/$', scrap_request),
]
