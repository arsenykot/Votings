from django.http import HttpResponse
from main.util import *
from main.models import *
import json

def test_api_view(req):
    return HttpResponse(json.dumps({"POST": req.POST, "GET": req.GET}, indent=2, ensure_ascii=False))

