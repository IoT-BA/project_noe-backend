from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.models import Gateway, Rawpoint, Point, Node, Key
from datetime import datetime
import csv
import json
import time

def index(request):
    return HttpResponse("Not much to see here mate!")

@csrf_exempt
def points_this_node(request, node_id):
    if request.method == 'GET':
        node = Node.objects.get(node_id = node_id)
        p_list = Point.objects.filter(node = node_id).order_by('-timestamp')[:100]
        out = {
            'dataset': [],
            'node': {
                'serial': node.id,
                'name': node.name,
                'owner': node.owner.username,
            }
        }
        for p in p_list:
            out['dataset'].append({
                'value': p.value,
                'timestamp': str(p.timestamp),
                'key_numeric': p.key.numeric,
                'key_description': p.key.key,
                'key_unit': p.key.unit,
            })
        if request.GET.get('format') == 'csv':
            response = HttpResponse(content_type='text/plain')
            writer = csv.writer(response)
            for p in p_list:
                writer.writerow([ p.timestamp, p.key.numeric, p.value ])
            return response
        else:
            pretty_json = json.dumps(out, indent=4)
            return HttpResponse(pretty_json, content_type="application/json")

def rawpoints_this_node(request, node_id):
    if request.method == 'GET':
        node = Node.objects.get(node_id = node_id)
        p_list = Rawpoint.objects.filter(node = node).order_by('-timestamp')[:1000]
        out = {
            'dataset': [],
            'node': {
                'backend_id': node.id,
                'node_id':    node.node_id,
                'name':       node.name,
                'owner':      node.owner.username,
            },
            'info': {
                'api_request_timestamp': str(time.time())
            },
        }
        for p in p_list:
            out['dataset'].append({
                'payload': p.payload,
                'datetime': str(p.timestamp),
                'timestamp': (p.timestamp.replace(tzinfo=None) - datetime(1970, 1, 1)).total_seconds(),
            })
        if request.GET.get('format') == 'csv':
            response = HttpResponse(content_type='text/plain')
            writer = csv.writer(response)
            for p in p_list:
                writer.writerow([ p.timestamp, p.key.numeric, p.value ])
            return response
        else:
            pretty_json = json.dumps(out, indent=4)
            return HttpResponse(pretty_json, content_type="application/json")

def points_this_node_key(request, node_id, key_numeric):
    if request.method == 'GET':
        if not request.GET.get('limit'):
            limit = 1000
        else:
            limit = request.GET.get('limit')
        key = Key.objects.get(numeric=key_numeric)
        node = Node.objects.get(id = node_id)
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

@csrf_exempt
def gis(request):
    ''' Output in GeoJSON format '''

    out = {
        'type': 'FeatureCollection',
        'features': []
    }
    for gw in Gateway.objects.all():
        out['features'].append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [ gw.gps_lat, gw.gps_lon ],
            },
            'properties': {
                'name': gw.description,
                'address': gw.location,
                'gps_lon': gw.gps_lon,
                'gps_lat': gw.gps_lat,
                'type': 'gateway'
            }
        })
    for node in Node.objects.all():
        out['features'].append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [ node.gps_lat, node.gps_lon ],
            },
            'properties': {
                'name': node.description,
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

def node_info(request, node_id):
    if request.method == 'GET':
        n = Node.objects.filter(node_id = node_id)[0]
        out = {
            'serial': n.id,
            'name': n.name,
            'location': n.location,
            'description': n.description,
            'owner': n.owner.username,
        }
        return JsonResponse(out, safe=False)

def rawpoints(request):
    if request.method == 'GET':
        p_list = Rawpoint.objects.all().order_by('-timestamp')[:1000]
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
                                       'payload': p.payload,
                                       'timestamp': str(p.timestamp),
                })
            pretty_json = json.dumps(out, indent=4)
            return HttpResponse(pretty_json, content_type="application/json")

@csrf_exempt
def save_point(request):
    from datetime import datetime 
    import pytz
    from pprint import pprint

    out = []

    if request.method == 'POST':
        pprint(request.body)
        data = json.loads(request.body)
        for d in data:
            try: 
                point = Rawpoint()
                point.payload = d['payload']
                #point.gw = Gateway.objects.get(serial = d['gateway_serial']) 
                point.node = Node.objects.get(node_id = d['node_id']) 
                point.rssi = d['rssi'] 
                try:
                    d['snr']
                    point.snr = d['snr'] 
                except Exception as e:
                    point.snr = None 
                point.timestamp = datetime.utcfromtimestamp(d['timestamp']).replace(tzinfo=pytz.utc) 
                point.save()
                out.append({ 'rowid': d['rowid'], 'status': 1 })
            except Exception as e:
                out.append({ 'rowid': d['rowid'],
                             'status': 2,
                             'status_explain': str(e)
                          })
        return JsonResponse(out, safe=False)
