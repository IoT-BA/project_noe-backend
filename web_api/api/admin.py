from django.contrib import admin
from api.models import Gateway
from api.models import Point 
from api.models import Node 

class PointAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'node_id', 'key', 'value')

class NodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')

admin.site.register(Gateway)
admin.site.register(Node, NodeAdmin)
admin.site.register(Point, PointAdmin)
