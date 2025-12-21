from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from main.util import *
from main.models import *
from time import time, sleep
from django.shortcuts import redirect

def test_api_view(req):
    return HttpResponse(str(req.user.is_authenticated))

def auth_login_view(req):
    #sleep(2)
    uname = getPostOr(req, "username", False)
    passwd = getPostOr(req, "password", False)
    status = 200
    text = "OK"
    if uname == False or passwd == False:
        status = 400
        text = "BADREQUEST"
    else:
        user = authenticate(req, username=uname, password=passwd)
        if user is None:
            text = "BADCREDENTIALS"
            status = 403
        else:
            login(req, user)
    resp = HttpResponse(text)
    resp.status_code = status
    return resp

def auth_logout_view(req):
    if req.user.is_authenticated:
        logout(req)
    return redirect("/")