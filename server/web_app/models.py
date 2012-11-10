from django.db import models
import datetime, sys
from djangotoolbox.fields import *

# Create your models here.

class BTActivity(models.Model):
    devID = models.IntegerField(blank=False)
    activityTime = models.DateTimeField(blank=False)
    activity = models.IntegerField(blank=False)


class BTDevice(models.Model):
    devID = models.IntegerField(blank=False)
    devName = models.CharField(max_length=64, blank=True)
    devLocLat = models.CharField(blank=False, max_length=20)
    devLocLong = models.CharField(blank=False, max_length=20)
    scanTime = models.DateTimeField(blank=False)


