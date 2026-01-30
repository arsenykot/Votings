from main.util import *
from django.shortcuts import redirect
from django.http import HttpResponse
from main.models import *

def report_list_view(req):
    return respond(501, "Not implemented")