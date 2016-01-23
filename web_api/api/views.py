from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from api.models import Point
import json

def index(request):
    return HttpResponse("Not much to see here mate!")

@csrf_exempt
def get(request, node_id, key):
    if request.method == 'GET':
        p_list = Point.objects.filter(node_id = node_id, key = key).values()
        out = {
            'dataset': [],
            'node_id': int(node_id),
            'key': int(key),
        }
        for point in p_list:
            out['dataset'].append({
                'value': point['value'],
                'timstamp': str(point['timestamp'])
            })
        return HttpResponse(json.dumps(out))
