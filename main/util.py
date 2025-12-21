from hashlib import sha256
from time import time
from django.contrib.auth.models import User
from django.http import HttpResponse

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