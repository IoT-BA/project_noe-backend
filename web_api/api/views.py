from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.models import Point, Node, Key

def index(request):
    return HttpResponse("Not much to see here mate!")

@csrf_exempt
def points_this_node(request, node_id):
    if request.method == 'GET':
        node = Node.objects.get(id = node_id)
        p_list = Point.objects.filter(node = node_id).order_by('-timestamp')[:10]
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
        return JsonResponse(out, safe=False)

def points_this_node_key(request, node_id, key_numeric):
    if request.method == 'GET':
        key = Key.objects.get(numeric=key_numeric)
        node = Node.objects.get(id = node_id)
        p_list = Point.objects.filter(node = node, key = key).order_by('-timestamp')
        out = {
            'dataset': [],
            'node_serial': node.id,
            'key': key.numeric,
        }
        for point in p_list:
            out['dataset'].append({
                'value': point.value,
                'timestamp': str(point.timestamp)
            })
        return JsonResponse(out, safe=False)

def points_all_nodes(request):
    if request.method == 'GET':
        p_list = Point.objects.all().order_by('-timestamp')[:30]
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
        n = Node.objects.filter(id = node_id)[0]
        out = {
            'serial': n.id,
            'name': n.name,
            'location': n.location,
            'description': n.description,
            'owner': n.owner.username,
        }
        return JsonResponse(out, safe=False)
