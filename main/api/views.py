from django.http import HttpResponse
from main.util import *
from main.models import *

def test_api_view(req):
    return HttpResponse(str(req.user.is_authenticated))

