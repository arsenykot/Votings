from django.contrib.auth import authenticate, login, logout
from time import time, sleep
from django.shortcuts import redirect
from main.util import *
from main.models import *
from django.http import HttpResponse
import re

def name_view(req):
    uname = getGetOr(req, "username", False)
    
    if uname == False:
        return respond(400, "BADREQUEST")
    uname = uname.lower()
    if not re.fullmatch(USERNAME_RE_MATCH, uname):
        return respond(400, "REGEX")
    if user_exists(uname):
        return respond(200, "TAKEN")
    
    return respond(200, "OK")

def register_view(req):
    uname = getPostOr(req, "username", False)
    passwd = getPostOr(req, "password", False)
    
    if uname == False or passwd == False:
        return respond(400, "BADREQUEST")
    uname = uname.lower()
    if not re.fullmatch(USERNAME_RE_MATCH, uname):
        return respond(400, "REGEX")
    if user_exists(uname):
        return respond(400, "USERNAMETAKEN")
    if len(uname) > 24 or len(uname) < 4:
        return respond(400, "BADREQUEST")
    if len(passwd) < 8:
        return respond(400, "PWDSHORT")
    if " " in uname:
        return respond(400, "BADREQUEST")
    
    u = User.objects.create_user(uname, "", passwd)
    login(req, u)
    return respond(200, "OK")