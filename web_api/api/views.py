from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.models import Point

def index(request):
    return HttpResponse("Not much to see here mate!")

@csrf_exempt
def batch(request, node_id, key):
    if request.method == 'GET':
        p_list = Point.objects.filter(node_id = node_id, key = key)
        out = {
            'dataset': [],
            'node_serial': int(node_id),
            'key': int(key),
        }
        for point in p_list:
            out['dataset'].append({
                'value': point.value,
                'timestamp': str(point.timestamp)
            })
        return JsonResponse(out, safe=False)

def last(request, node_id, key):
    if request.method == 'GET':
        p = Point.objects.filter(node = node_id, key = key).order_by('-timestamp')[0]
        out = {
            'value': p.value,
            'timestamp': str(p.timestamp),
            'key': p.key,
            'node': {
                'name': p.node.name,
                'description': p.node.description,
                'serial': p.node.id,
            },
        }
        return JsonResponse(out, safe=False)

def last_this_node(request, node_id):
    if request.method == 'GET':
        p = Point.objects.filter(node = node_id).order_by('-timestamp')[0]
        out = {
            'value': p.value,
            'timestamp': str(p.timestamp),
            'key': p.key,
            'node': {
                'name': p.node.name,
                'description': p.node.description,
                'serial': p.node.id,
                'responsible': p.node.responsible,
            },
        }
        return JsonResponse(out, safe=False)

def last_all_nodes(request):
    if request.method == 'GET':
        points = Point.objects.all().order_by('-timestamp')[:30]
        out = []
        for p in points:
            out.append({
                'value': p.value,
                'timestamp': str(p.timestamp),
                'key': p.key,
                'node_serial': p.node_id,
            })
        return JsonResponse(out, safe=False)
