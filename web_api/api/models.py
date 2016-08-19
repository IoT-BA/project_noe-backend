from django.db import models
from django.contrib.auth.models import User

class Gateway(models.Model):
    def __unicode__(self):
         return str(self.id) + " - " + self.description
    description = models.CharField(max_length=128)
    owner = models.ForeignKey(User)
    location = models.CharField(max_length=512, default="", blank=True)
    gps_lon = models.FloatField(default=0.0, blank=True)
    gps_lat = models.FloatField(default=0.0, blank=True)
    serial = models.CharField(max_length=128, default="", blank=True)

class Key(models.Model):
    def __unicode__(self):
         return str(self.numeric) + " ~ " + self.key + " ~ " + self.unit
    numeric = models.IntegerField(primary_key=True)
    key = models.CharField(max_length=256, default="?")
    unit = models.CharField(max_length=256, default="?")

class Node(models.Model):
    def __unicode__(self):
         return str(self.node_id) + " - " + self.owner.first_name + " " + self.owner.last_name
    id = models.AutoField(primary_key = True)
    node_id = models.CharField(max_length=256, null=True)
    name = models.CharField(max_length=128, default="")
    location = models.CharField(max_length=512, default="")
    description = models.TextField()
    owner = models.ForeignKey(User)
    gps_lon = models.FloatField(default=0.0)
    gps_lat = models.FloatField(default=0.0)

class Point(models.Model):
    def __unicode__(self):
         return str(self.id)
    id = models.IntegerField(primary_key = True)
    key = models.ForeignKey(Key, db_column = '_key', db_constraint=False)
    node = models.ForeignKey(Node, db_column = 'serial', db_constraint=False)
    value = models.IntegerField()
    rssi = models.IntegerField(null=True)
    timestamp = models.DateTimeField()
    gw = models.ForeignKey(Gateway, db_constraint=False, null=True)
    raw_packet = models.CharField(max_length=256)
    class Meta:
        db_table = 'parsed_data'

class Rawpoint(models.Model):
    def __unicode__(self):
         return str(self.id)
    id = models.IntegerField(primary_key = True)
    payload = models.CharField(max_length=128)
    gateway_serial = models.CharField(max_length=128, null=True)
    gw = models.ForeignKey(Gateway, db_column = 'gw_serial', null=True)
    rssi = models.IntegerField(null=True, blank=True)
    snr = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(db_column = 'gw_timestamp')
    node = models.ForeignKey(Node)
    class Meta:
        db_table = 'raw_data'
