from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from api.models import Gateway
from api.models import Point 
from api.models import Node 
from api.models import NodeType
from api.models import Key
from api.models import Rawpoint
from api.models import Profile 
from api.models import LoRaWANRawPoint 
from api.models import LoRaWANApplication 

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )

class GatewayAdmin(admin.ModelAdmin):
    list_display = ('id', 'mac', 'owner', 'serial', 'location', 'gps_lon', 'gps_lat')

class RawpointAdmin(admin.ModelAdmin):
    list_display = ('id', 'seq_number', 'timestamp', 'payload', 'rssi', 'snr', 'node_id', 'gw', 'gateway_serial', 'state')
    list_filter = ('node_id', 'gw', 'gateway_serial')

class LoRaWANRawPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'DevAddr')
    list_filter = ('DevAddr', 'datr', 'chan')

class PointAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'node_id', 'key', 'value', 'rssi', 'gw')
    list_filter = ('gw', 'node_id', 'key') 
    search_fields = ('gw__description', 'node__name')
    raw_id_fields = ('rawpoint', )

class KeyAdmin(admin.ModelAdmin):
    list_display = ('numeric', 'key', 'unit')

class NodeAdmin(admin.ModelAdmin):
    list_display = ('node_id', 'owner', 'name', 'description', 'api_key', 'nodetype')

admin.site.register(Gateway, GatewayAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(NodeType)
admin.site.register(Key, KeyAdmin)
admin.site.register(Point, PointAdmin)
admin.site.register(Rawpoint, RawpointAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(LoRaWANRawPoint, LoRaWANRawPointAdmin)
admin.site.register(LoRaWANApplication)
