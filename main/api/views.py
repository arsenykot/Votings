from django.http import HttpResponse

def test_api_view(req):
    return HttpResponse("Hello, World!")