from main.util import *
from django.shortcuts import redirect
from django.http import HttpResponse
from main.models import *

def users_list(req):
    if not req.user.is_staff:
        return redirect("/")
    return render(req, "staff/users.html")

def reports_list(req):
    if not req.user.is_staff:
        return redirect("/")
    return render(req, "staff/reports.html")