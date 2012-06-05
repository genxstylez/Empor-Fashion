from django.http import HttpResponse
from django.utils import simplejson as json

def JSONResponse(dict):
    return HttpResponse(json.dumps(dict), mimetype='application/json')
