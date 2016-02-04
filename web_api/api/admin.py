from django.contrib import admin
from api.models import Gateway
from api.models import Point 
from api.models import Node 
from api.models import Key

class GatewayAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'location')

class PointAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'node_id', 'key', 'value', 'rssi')

class KeyAdmin(admin.ModelAdmin):
    list_display = ('numeric', 'key', 'unit')

class NodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'name', 'description')

admin.site.register(Gateway, GatewayAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(Key, KeyAdmin)
admin.site.register(Point, PointAdmin)
