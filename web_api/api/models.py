from django.db import models

class Gateway(models.Model):
    def __unicode__(self):
         return self.description
    description = models.CharField(max_length=128)

class Node(models.Model):
    def __unicode__(self):
         return self.description
    name = models.CharField(max_length=128, default="")
    description = models.CharField(max_length=128)

class Point(models.Model):
    def __unicode__(self):
         return str(self.id)
    id = models.IntegerField(primary_key = True)
    key = models.IntegerField(db_column = '_key')
    node_id = models.ForeignKey(Node, db_column = 'serial')
    value = models.IntegerField()
    timestamp = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'parsed_data'


# Create your models here.
