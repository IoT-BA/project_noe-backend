from django.contrib import admin
from api.models import Gateway
from api.models import Point 
from api.models import Node 
from api.models import Key
from api.models import Rawpoint

class GatewayAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'owner', 'serial', 'location')

class RawpointAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'payload', 'rssi', 'node_id', 'gw')
    list_filter = ('node_id', 'gw')

class PointAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'node_id', 'key', 'value', 'rssi', 'gw')
    list_filter = ('gw', 'node_id', 'key') 
    search_fields = ('gw__description', 'node__name')

class KeyAdmin(admin.ModelAdmin):
    list_display = ('numeric', 'key', 'unit')

class NodeAdmin(admin.ModelAdmin):
    list_display = ('node_id', 'owner', 'name', 'description')

admin.site.register(Gateway, GatewayAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(Key, KeyAdmin)
admin.site.register(Point, PointAdmin)
admin.site.register(Rawpoint, RawpointAdmin)
