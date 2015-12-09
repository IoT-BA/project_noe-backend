from django.db import models


class Gateway(models.Model):
    def __unicode__(self):
         return self.description
    description = models.CharField(max_length=128)

class Point(models.Model):
    def __unicode__(self):
         return self.payload
    payload = models.CharField(max_length=64)

# Create your models here.
