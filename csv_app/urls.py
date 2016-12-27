from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^update/$', views.csv_update),
    url(r'^retrive/(?P<deviceid>\w+)/$', views.retrive_deviceid),
    url(r'^retrive/(?P<deviceid>\w+)/(?P<gte>[0-9]+)/(?P<lte>[0-9]+)/$',
        views.retrive),
]
