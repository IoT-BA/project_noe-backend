import csv
import json
import time
import pytz
import base64
import struct
from lora.crypto import loramac_decrypt

from api.models import User, NodeType, Profile, Gateway, LoRaWANRawPoint, Rawpoint, Point, Node, Key

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime
import dateutil.parser
from pprint import pprint

def index(request):
    return HttpResponse("Not much to see here mate!")

@csrf_exempt
def user_login(request):
    logout(request)
    username = password = ''
    if request.GET:
        username = request.GET.get('username')
        password = request.GET.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                out = {
                          'user_access_key': str(user.profile.user_api_key),
                          'login': 'ok',
                      }
                pretty_json = json.dumps(out, indent=4)
                return HttpResponse(pretty_json, content_type="application/json")
    out = {
              'login': 'failed',
          }
    pretty_json = json.dumps(out, indent=4)
    return HttpResponse(pretty_json, content_type="application/json", status=401)

@csrf_exempt
def points_this_node(request, node_api_key):
    if request.method == 'GET':
        node = Node.objects.get(api_key = node_api_key)
        p_list = Point.objects.filter(node = node).order_by('-timestamp')[:200]
        out = {
            'dataset': [],
            'node': {
                'serial': node.id,
                'name': node.name,
                'owner': node.owner.username,
            }
        }
        for p in p_list:
            try:
                out['dataset'].append({
                    'value': p.value,
                    'timestamp': str(p.timestamp),
                    'key_numeric': p.key.numeric,
                    'key_description': p.key.key,
                    'key_unit': p.key.unit,
                })
            except Exception as e:
                # probably no such key
                continue
        if request.GET.get('format') == 'csv':
            response = HttpResponse(content_type='text/plain')
            writer = csv.writer(response)
            for p in p_list:
                try:
                    writer.writerow([ p.timestamp, p.key.numeric, p.value ])
                except Exception as e:
                    # probably no such key
                    continue
            return response
        else:
            pretty_json = json.dumps(out, indent=4)
            return HttpResponse(pretty_json, content_type="application/json")

def rawpoints_this_node(request, node_api_key):
    if request.method == 'GET':
        if not request.GET.get('limit'):
            limit = 3000
        else:
            limit = request.GET.get('limit')
        node = Node.objects.get(api_key = node_api_key)
        p_list = Rawpoint.objects.filter(node = node).order_by('-timestamp').distinct()[:limit]
        out = {
            'dataset': [],
            'node': {
                'backend_id': node.id,
                'node_id':    node.node_id,
                'name':       node.name,
                'owner':      node.owner.username,
                'nodetype':   node.nodetype.name,
            },
            'info': {
                'api_request_timestamp': str(timezone.now()),
                'dataset_size_limit': limit,
                'dataset_size': len(p_list),
            },
        }

        seq_number_min = 999999999;
        seq_number_max = 0;
        sequenced_points = 0

        for p in p_list:
            if not (p.seq_number is None):
                if p.seq_number < seq_number_min:
                    seq_number_min = p.seq_number
                if p.seq_number > seq_number_max:
                    seq_number_max = p.seq_number
                sequenced_points = sequenced_points + 1
            out['dataset'].append({
                'payload': p.payload,
                'seq_number': p.seq_number,
                'datetime': str(p.timestamp),
                'timestamp': (p.timestamp.replace(tzinfo=None) - datetime(1970, 1, 1)).total_seconds(),
            })

        delta_sequence = seq_number_max - seq_number_min
        out['info']['loss_rate_percent'] = round(100 - (100.0 / float(delta_sequence) * float(sequenced_points)), 1)

        out['info']['seq_delta'] = delta_sequence 
        out['info']['sequenced_points'] = sequenced_points
        out['info']['seq_number_min'] = seq_number_min
        out['info']['seq_number_max'] = seq_number_max

        if request.GET.get('format') == 'csv':
            response = HttpResponse(content_type='text/plain')
            writer = csv.writer(response)
            for p in p_list:
                writer.writerow([ p.timestamp, p.key.numeric, p.value ])
            return response
        else:
            pretty_json = json.dumps(out, indent=4)
            return HttpResponse(pretty_json, content_type="application/json")

def rssi_this_node(request, node_api_key):
    if request.method == 'GET':
        if not request.GET.get('limit'):
            limit = 200
        else:
            limit = request.GET.get('limit')
        node = Node.objects.get(api_key = node_api_key)
        p_list = Rawpoint.objects.filter(node = node).order_by('-timestamp')[:limit]
        out = {
            'dataset': [],
            'node': {
                'backend_id': node.id,
                'node_id':    node.node_id,
                'name':       node.name,
                'owner':      node.owner.username,
                'nodetype':   node.nodetype.name,
            },
            'info': {
                'api_request_timestamp': str(timezone.now()),
                'dataset_size_limit': limit,
                'dataset_size': len(p_list),
            },
        }
        for p in p_list:
            out['dataset'].append({
                'datetime': str(p.timestamp),
                'timestamp': int((p.timestamp.replace(tzinfo=None) - datetime(1970, 1, 1)).total_seconds()),
                'rssi': p.rssi,
                'snr': p.snr,
                'gateway_serial': p.gateway_serial,
            })
        pretty_json = json.dumps(out, indent=4)
        return HttpResponse(pretty_json, content_type="application/json")

def points_this_node_key(request, node_api_key, key_numeric):
    if request.method == 'GET':
        if not request.GET.get('limit'):
            limit = 1000
        else:
            limit = request.GET.get('limit')
        key = Key.objects.get(numeric=key_numeric)
        node = Node.objects.get(api_key = node_api_key)
        p_list = Point.objects.filter(node = node, key = key).order_by('-timestamp')[:limit]
        out = {
            'dataset': [],
            'node_serial': node.id,
            'key': key.numeric,
        }
        for point in p_list:
            out['dataset'].append({
                'value': point.value,
                'timestamp': str(point.timestamp),
                'rssi': point.rssi
            })
        if request.GET.get('format') == 'csv':
            response = HttpResponse(content_type='text/plain')
            writer = csv.writer(response)
            i = 0
            for p in p_list:
                writer.writerow([ i, p.timestamp, p.key.numeric, p.value ])
                i = i + 1
            return response
        else:
            return JsonResponse(out, safe=False)

def nodes(request):
    ''' List of all Nodes '''

    out = { 'nodes': [] }

    for node in Node.objects.all().order_by('name'):
        out['nodes'].append({
            'name': node.name,
            'description': node.description,
            'api_key': node.api_key,
        })

    pretty_json = json.dumps(out, indent=4)
    response = HttpResponse(pretty_json, content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    return response

def gws_list(request):
    ''' List of all Gateways '''

    out = { 'gws': [] }

    for gw in Gateway.objects.all().order_by('description'):
        out['gws'].append({
            'description': gw.description,
            'serial': gw.serial,
            'owner': gw.owner.username,
            'last_seen': str(gw.last_seen),
            'gps_lon': gw.gps_lon,
            'gps_lat': gw.gps_lat,
        })

    pretty_json = json.dumps(out, indent=4)
    response = HttpResponse(pretty_json, content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    return response

def lorawan_points_all(request):
    ''' All LoRaWAN raw points, but try to decrypt them '''

    out = { 'points': [] }
    for point in LoRaWANRawPoint.objects.all().order_by('-id')[:1000]:

        p = {}

        p['id'] = point.id
        p['FRMPayload'] = point.FRMPayload
        p['FCnt'] = point.FCnt
        p['FPort'] = point.FPort
        p['DevAddr'] = point.DevAddr

        MTypes = (
                     'Join Request',
                     'Join Accept',
                     'Unconfirmed Data Up',
                     'Unconfirmed Data Down',
                     'Confirmed Data Up',
                     'Confirmed Data Down',
                     'RFU',
                     'Proprietary',
                 )

        if point.MType:
            p['MType_description'] = MTypes[point.MType]
        else:
            pass 

        try:
            # LoRaWAN spec 1.0; section 4.3.3.1
            if point.FPort == 0:
                SKey = point.node.lorawan_NwkSKey
                p['SKey_used'] = 'NwkSKey'
                p['NwkSKey'] = point.node.lorawan_NwkSKey
            else:
                SKey = point.node.lorawan_AppSKey
                p['SKey_used'] = 'AppSKey'
                p['AppSKey'] = point.node.lorawan_AppSKey
            FRMPayload_decrypted = ""
            FRMPayload_decrypted = loramac_decrypt(point.FRMPayload, point.FCnt, SKey, point.DevAddr)
            p['FRMPayload_decrypted'] = "".join("{:02x}".format(c) for c in FRMPayload_decrypted)
        except Exception as e:
            p['error'] = "Unable to decrypt LoRaWAN packet " + str(e)


        out['points'].append(p)

    pretty_json = json.dumps(out, indent=4)
    response = HttpResponse(pretty_json, content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    return response

def user_info(request, username):
    ''' User details '''

    user = User.objects.get(username = username)

    out = {
            'name': user.username,
            'nodes': [],
            'nodes_own': [],
            'gws': [],
          }

    for node in Node.objects.filter(users = user).order_by('name'):
        if (node.last_rawpoint == None):
            last_rawpoint = "2000-11-11 11:11:11+00:00"
        else:
            last_rawpoint = str(node.last_rawpoint)
        out['nodes'].append({
            'name': node.name,
            'type': node.nodetype.name,
            'id': node.node_id,
            'api_key': node.api_key,
            'last_rawpoint': last_rawpoint,
        }) 

    for node in Node.objects.filter(owner = user).order_by('name'):
        if (node.last_rawpoint == None):
            last_rawpoint = "2000-11-11 11:11:11+00:00"
        else:
            last_rawpoint = str(node.last_rawpoint)
        out['nodes_own'].append({
            'name': node.name,
            'type': node.nodetype.name,
            'id': node.node_id,
            'api_key': node.api_key,
            'last_rawpoint': last_rawpoint,
        }) 

    for gw in Gateway.objects.filter(owner = user).order_by('mac'):
        out['gws'].append({
            'mac': gw.mac,
            'serial': gw.serial,
            'last_seen': str(gw.last_seen),
            'position': { 'lon': gw.gps_lon, 'lat': gw.gps_lat },
        }) 

    pretty_json = json.dumps(out, indent=4)
    response = HttpResponse(pretty_json, content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    return response

def users(request):
    ''' List of all Users '''

    out = { 'users': [] }

    for user in User.objects.all().order_by('username'):
        u = {
            'name': user.username,
            'email': user.email,
            'nodes': [],
        }

        try:
            u['user_api_key'] = user.profile.user_api_key
        except Exception as e:
            u['user_api_key'] = "" 

        try:
            u['phone'] = user.profile.phone_number
        except Exception as e:
            u['phone'] = "" 

        for node in Node.objects.filter(owner = user):
            u['nodes'].append({ 'name': node.name, 'api_key': node.api_key }) 
        out['users'].append(u)

    pretty_json = json.dumps(out, indent=4)
    response = HttpResponse(pretty_json, content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    return response

@csrf_exempt
def gis(request):
    ''' Output in GeoJSON format '''

    out = {
        'type': 'FeatureCollection',
        'features': []
    }
    for gw in Gateway.objects.all():
        if (gw.gps_lon == 0) or (gw.gps_lat == 0):
            continue
        out['features'].append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [ gw.gps_lon, gw.gps_lat ],
            },
            'properties': {
                'name': str(gw.description) + " ID: " +  str(gw.id),
                'address': str(gw.location),
                'gps_lon': gw.gps_lon,
                'gps_lat': gw.gps_lat,
                'type': 'gateway',
                'last_seen': str(gw.last_seen),
            }
        })
    for node in Node.objects.all():
        continue
        out['features'].append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [ node.gps_lon, node.gps_lat ],
            },
            'properties': {
                'name': str(node.description),
                'address': node.location,
                'node_id': node.node_id,
                'type': 'node',
                'gps_lon': node.gps_lon,
                'gps_lat': node.gps_lat
            }
        })
    pretty_json = json.dumps(out, indent=4)
    response = HttpResponse(pretty_json, content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    return response

def points_all_nodes(request):
    if request.method == 'GET':
        p_list = Point.objects.all().order_by('-timestamp')[:1000]
        out = []
        for p in p_list:
            out.append({
                'value': p.value,
                'timestamp': str(p.timestamp),
                'key': p.key.numeric,
                'node': {
                    'serial': p.node.id,
                    'owner': p.node.owner.username,
                }
            })
        return JsonResponse(out, safe=False)

def points_all_nodes_key(request, key_numeric):
    if request.method == 'GET':
        key = Key.objects.get(numeric=key_numeric)
        p_list = Point.objects.filter(key = key).order_by('-timestamp')[:1000]
        out = []
        for p in p_list:
            out.append({
                'value': p.value,
                'timestamp': str(p.timestamp),
                'key': p.key.numeric,
                'node': {
                    'serial': p.node.id,
                    'owner': p.node.owner.username,
                }
            })
        return JsonResponse(out, safe=False)

@csrf_exempt
def gw_register(request, gw_mac):
    if request.method == 'POST':
        out = {
            'serial': 'b827ebfffed1fcc2',
            'mac': gw_mac
        }
    else:
        pretty_json = json.dumps({ 'error': 'GET call does not exist on this URI - try POST request' }, indent=4)
        response = HttpResponse(pretty_json, content_type="application/json",  status=400)
        response['Access-Control-Allow-Origin'] = '*'
        return response

    pretty_json = json.dumps(out, indent=4)
    response = HttpResponse(pretty_json, content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    return response

def gw_info(request, gw_serial):
    if request.method == 'GET':
        try:
            gw = Gateway.objects.get(serial = gw_serial)
        except Exception as e:
            pretty_json = json.dumps({ 'error': 'no such gateway in the database', "gw_serial": gw_serial }, indent=4)
            response = HttpResponse(pretty_json, content_type="application/json",  status=400)
            response['Access-Control-Allow-Origin'] = '*'
            return response
        out = {
            'id': gw.id,
            'serial': gw.serial,
            'mac': gw.mac,
            'description': gw.description,
            'owner': { 'username': gw.owner.username }, 
            'last_seen': str(gw.last_seen),
        }

    pretty_json = json.dumps(out, indent=4)
    response = HttpResponse(pretty_json, content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    return response

def node_info(request, node_api_key):
    if request.method == 'GET':
        n = Node.objects.get(api_key = node_api_key)
        out = {
            'serial': n.id,
            'node_id': n.node_id,
            'name': n.name,
            'location': n.location,
            'description': n.description,
            'owner': n.owner.username,
            'api_key': n.api_key,
            'nodetype': n.nodetype.name,
            'gps_lon': n.gps_lon,
            'gps_lat': n.gps_lat,
            'last_rawpoint': str(n.last_rawpoint),
            'keys': [],
            'key_numeric': {},
        }

        for key in n.nodetype.keys.all():
            out['keys'].append( { 'numeric': key.numeric, 'name': key.key, 'unit': key.unit } )
            out['key_numeric'][str(key.numeric)] = { 'numeric': key.numeric, 'name': key.key, 'unit': key.unit }

    pretty_json = json.dumps(out, indent=4)
    response = HttpResponse(pretty_json, content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    return response

def rawpoints(request):
    if request.method == 'GET':
        if not request.GET.get('limit'):
            limit = 200
        else:
            limit = request.GET.get('limit')
        p_list = Rawpoint.objects.all().order_by('-timestamp')[:limit]
        if request.GET.get('format') == 'csv':
            response = HttpResponse(content_type='text/plain')
            writer = csv.writer(response)
            for p in p_list:
                writer.writerow([ p.gw.description, p.timestamp, p.payload, p.rssi ])
            return response
        else:
            out = { 'dataset': [] }
            for p in p_list:
                out['dataset'].append({
                                          'rawpoint_id': str(p.id),
                                          'payload':     str(p.payload),
                                          'datetime':    str(p.timestamp),
                                          'node': {
                                              'api_key':  str(p.node.api_key),
                                              'nodetype': str(p.node.nodetype.name),
                                          },
                                     })
            pretty_json = json.dumps(out, indent=4)
            return HttpResponse(pretty_json, content_type="application/json")

@csrf_exempt
def gw_update(request):

    if request.method != 'POST':
        pretty_json = json.dumps({ 'error': str(request.method) + ' call does not exist on this URI' }, indent=4)
        response = HttpResponse(pretty_json, content_type="application/json",  status=400)
        response['Access-Control-Allow-Origin'] = '*'
        return response

    try:
        d = json.loads(request.body)
    except Exception as e:
        out = { 'satus': 1, 'status': str(e.args), 'status_explain': 'unable to parse json from POST payload' }
        status_code = 400
        return JsonResponse(out, safe=False, status=status_code)

    try:
        gw = Gateway.objects.get(mac = d['mac'])
    except Exception as e:
        print("Error: " + str(e))
        print("Creating new Gateway with MAC " + d['mac'])
        gw = Gateway(
                     mac = d['mac'],
                     owner = User.objects.get(username = 'unclaimed')
                    )
    else:
        print("Gateway found with ID: " + str(gw.id))

    gw.gps_lon = d['longitude']
    gw.gps_lat = d['latitude']
    gw.last_seen = timezone.now()
    gw.save()

    out = { 'satus': 1, 'gw_mac': gw.mac, 'gw_serial': gw.serial }
    return JsonResponse(out, safe=False, status=200)

@csrf_exempt
def save_rawpoint(request):

    out = []
    status_code = 200

    if request.method != 'POST':
        pretty_json = json.dumps({ 'error': str(request.method) + ' call does not exist on this URI' }, indent=4)
        response = HttpResponse(pretty_json, content_type="application/json",  status=400)
        response['Access-Control-Allow-Origin'] = '*'
        return response

    try:
        data = json.loads(request.body)
    except Exception as e:
        out = { 'satus': 3, 'status': str(e.args), 'status_explain': 'unable to parse json from POST payload' }
        status_code = 400
        return JsonResponse(out, safe=False, status=status_code)

    i = 0
    for d in data:
        i = i + 1
        try: 
            point = Rawpoint()
            point.payload = d['payload']

            try:
                point.gw = Gateway.objects.get(mac = d['gw_mac']) 
            except Exception as e:
                pass

            try:
                point.gateway_serial = d['gateway_serial']
            except Exception as e:
                pass

            try:
                node = Node.objects.get(node_id = d['node_id'])
                node.last_rawpoint = timezone.now()
                node.save()
            except Exception as e:
                print("Creating new Node with node_id " + d['node_id'])
                node = Node(
                             node_id = d['node_id'],
                             nodetype = NodeType.objects.get(name = 'unknown'),
                             owner = User.objects.get(username = 'unclaimed')
                       )
                node.last_rawpoint = timezone.now()
                node.save()

            point.node = node

            try:
                d['rssi']
                point.rssi = d['rssi'] 
            except Exception as e:
                point.rssi = None

            try:
                point.seq_number = d['seq_number'] 
            except Exception as e:
                point.seq_number = None 

            try:
                d['snr']
                point.snr = d['snr'] 
            except Exception as e:
                point.snr = None 

            try:
                d['rowid']
            except Exception as e:
                d['rowid'] = i

            point.timestamp = datetime.fromtimestamp(d['timestamp'], pytz.utc)
            point.save()
            out.append({ 'rowid': d['rowid'], 'status': 1, 'status_human': 'OK' })
        except Exception as e:
            out.append({
                         'status': 2,
                         'status_explain': str(e.args),
                         'point_data': d,
                         'rowid': i
                      })
            status_code = 400
    return JsonResponse(out, safe=False, status=status_code)

@csrf_exempt
def save_point(request):
    from datetime import datetime 

    out = []

    if request.method == 'POST':
        data = json.loads(request.body)
        for d in data:
            print("Saving Point from following source data:")
            pprint(d)
            try: 
                point = Point()
                point.node = Node.objects.get(api_key = d['node_api_key'])
                point.rawpoint = Rawpoint.objects.get(id = d['rawpoint_id'])
                point.key = Key.objects.get(numeric = d['key'])
                point.value = d['value']
                point.rssi = 0
                point.timestamp = dateutil.parser.parse(d['datetime'])
                point.save()
                out.append({ 'rowid': d['rowid'], 'status': 1 })
            except Exception as e:
                out.append({ 'rowid': d['rowid'],
                             'status': 2,
                             'status_explain': str(e)
                          })
        return JsonResponse(out, safe=False)

@csrf_exempt
def save_lorawanrawpoint(request):
    from datetime import datetime 

    out = []

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except Exception as e:
            return JsonResponse([{
                    'status': 'unable to parse request body to JSON',
                    'string': str(request.body),
                }], safe=False)
        for d in data['i']['rxpk']:
            try: 
                point = LoRaWANRawPoint()
                point.chan = d['chan'] 
                point.codr = d['codr'] 
                point.data = d['data'] 
                point.datr = d['datr'] 
                point.freq = d['freq'] 
                point.lsnr = d['lsnr'] 
                point.rssi = d['rssi'] 
                point.time = dateutil.parser.parse(d['time'])
                point.tmst = d['tmst'] 
                point.gateway_serial = data['gateway_mac_ident'] 

                PHYPayload = []
                for c in base64.decodestring(d['data']):
                    PHYPayload.append(ord(c))
                MHDR        = PHYPayload[0]
                point.MType = int(MHDR >> 5)
                MACPayload  = PHYPayload[1:-4]

                FHDR        = MACPayload[:7]
                FRMPayload  = MACPayload[8:]

                point.PHYPayload = "".join("{:02x}".format(c) for c in PHYPayload)

                point.FPort      = int(MACPayload[7])
                point.MIC        = "".join("{:02x}".format(c) for c in PHYPayload[-4:])
                point.FRMPayload = "".join("{:02x}".format(c) for c in PHYPayload[1:-4][8:])

                # LoRaWAN 1.0, section 4.3.1
                point.DevAddr = "".join("{:02x}".format(FHDR[c]) for c in range(3,-1,-1))
                point.FCtrl   = "{:02x}".format(FHDR[4])
                point.FCnt    = struct.unpack("<H", "".join(chr(c) for c in FHDR[5:7]))[0]
                point.FOpts   = "".join("{:02x}".format(FHDR[c]) for c in FHDR[7:])

                try:
                    point.gw = Gateway.objects.get(serial = data['gateway_mac_ident'])
                except Exception as e:
                    pass

                try:
                    point.node = Node.objects.get(node_id = point.DevAddr)
                    point.node.lorawan_FCntUp = point.node.lorawan_FCntUp + 1
                    point.node.save()
                except Exception as e:
                    print(str(e))
                    pass

                point.save()
                out.append({
                        'status': 'saved'
                    })
            except Exception as e:
                out.append({
                        'status': 'save failed',
                        'status_explain': str(e),
                        'currently processing': str(json.dumps(d))
                    })
                pprint(out)
                raise
        return JsonResponse(out, safe=False)
