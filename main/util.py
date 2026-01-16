from hashlib import sha256
from time import time
from main.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
import re

USERNAME_RE_MATCH = re.compile(r"^([a-z0-9\.]{4,24})$")

def getArgumentOr(args, name, default):
    if(name in args.keys()):
        return args[name]
    return default

def getGetOr(req, name, default):
    return getArgumentOr(req.GET, name, default)

def getPostOr(req, name, default):
    return getArgumentOr(req.POST, name, default)

def getSessOr(req, name, default):
    return getArgumentOr(req.session, name, default)

def saltedHash(string, salt):
    return sha256(
        sha256(bytes(
            string, 
            encoding="utf-8"
            )).digest()+
            bytes(salt, encoding="utf-8")
        ).hexdigest()

def user_exists(username):
    return len(User.objects.filter(username=username)) > 0

def respond(status, data):
    r = HttpResponse(data)
    r.status_code = status
    return r

def containsAny(haystack, needles):
    for needle in needles:
        if needle in haystack:
            return True
    return False

def checkVars(data_list):
    for entry in data_list:
        val = None
        min = None
        max = None
        valid_items = None

        if type(entry[0]) is list:
            valid_items = entry[0]
            val = type(valid_items[0])(entry[1])
        else:
            try:
                val = entry[0](entry[1])
            except:
                return False
        
        if len(entry) > 2:
            min = entry[2]
        else:
            min = -1
        
        if len(entry) > 3:
            max = entry[3]
        
        if valid_items != None:
            if not val in valid_items:
                return False
        
        if entry[0] == int or entry[0] == float:
            if max == None:
                max = val
            if valid_items == None:
                if not (min <= val <= max):
                    return False
        
        elif entry[0] == str:
            if max == None:
                max = len(val)
            
            if valid_items == None:
                if not (min <= len(val) <= max):
                    return False
                if len(entry) > 4:
                    if not re.match(entry[4], val):
                        return False
        
    return True

def check_auth(auth = True, bans = True, redir = True):
    def decorator(func):
        def wrap(*args, **kwargs):
            req = args[0]
            if auth and not req.user.is_authenticated:
                if redir:
                    return redirect("/account/login")
                else:
                    return respond(401, "UNAUTHORIZED")
            if req.user.is_authenticated:
                if bans and req.user.is_banned:
                    if redir:
                        return redirect("/account/banned")
                    else:
                        return respond(403, "FORBIDDEN")
            return func(*args, **kwargs)
        return wrap
    return decorator