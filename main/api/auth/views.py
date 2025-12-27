from django.contrib.auth import authenticate, login, logout
from time import time, sleep
from django.shortcuts import redirect
from main.util import *
from main.models import *
from django.http import HttpResponse

def login_view(req):
    uname = getPostOr(req, "username", False)
    passwd = getPostOr(req, "password", False)
    if uname == False or passwd == False:
        return respond(400, "BADREQUEST")
    uname = uname.lower()
    user = authenticate(req, username=uname, password=passwd)
    if user is None:
        return respond(403, "BADCREDENTIALS")
    login(req, user)
    return respond(200, "OK")

def logout_view(req):
    if req.user.is_authenticated:
        logout(req)
    return redirect("/")