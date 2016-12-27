from django.db import models

# Create your models here.


class document(models.Model):
    t = models.DateTimeField(null=True, blank=True)
    deviceId = models.CharField(null=True, blank=True, max_length=100)
    label = models.CharField(null=True, blank=True, max_length=100)
    loc = models.CharField(null=True, blank=True, max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    AQI = models.FloatField(null=True, blank=True)
    PM10 = models.FloatField(null=True, blank=True)
    PM25 = models.FloatField(null=True, blank=True)
    CO = models.FloatField(null=True, blank=True)
    O3 = models.FloatField(null=True, blank=True)
    SO2 = models.FloatField(null=True, blank=True)
    NO2 = models.FloatField(null=True, blank=True)
    temp = models.FloatField(null=True, blank=True)
    hum = models.FloatField(null=True, blank=True)
    WD = models.FloatField(null=True, blank=True)
    WS = models.FloatField(null=True, blank=True)
    pressure = models.FloatField(null=True, blank=True)
    rainGaige = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['t']
