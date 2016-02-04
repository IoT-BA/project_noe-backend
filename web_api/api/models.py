from django.db import models
from django.contrib.auth.models import User

class Gateway(models.Model):
    def __unicode__(self):
         return self.description
    description = models.CharField(max_length=128)
    owner = models.ForeignKey(User)
    location = models.CharField(max_length=512, default="")

class Node(models.Model):
    def __unicode__(self):
         return str(self.id) + " - " + self.owner.username
    name = models.CharField(max_length=128, default="")
    location = models.CharField(max_length=512, default="")
    description = models.TextField()
    owner = models.ForeignKey(User)

class Point(models.Model):
    def __unicode__(self):
         return str(self.id)
    id = models.IntegerField(primary_key = True)
    key = models.IntegerField(db_column = '_key')
    node = models.ForeignKey(Node, db_column = 'serial')
    value = models.IntegerField()
    rssi = models.IntegerField()
    timestamp = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'parsed_data'

# Create your models here.
