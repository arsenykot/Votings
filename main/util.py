from main.models import User
from hashlib import sha256
from time import time
from django.shortcuts import render as raw_render

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

def grantNewToken(user: User):
    tok = saltedHash(user.username, user.token + str(time))
    user.token = tok
    user.save()
    return tok

def checkUser(username, token):
    if username == False or token == False:
        return False
    return len(User.objects.filter(username=username, token=token))>0

def render(request, template, context = None, content_type = None, status = None, using = None):
    newContext = {
        "logged_in" : checkUser(getSessOr(request, "username", False), getSessOr(request, "token", False)),
        "username" : getSessOr(request, "username", False)
    }
    for k in context.keys():
        newContext[k] = context[k]
    return raw_render(request, template, newContext, content_type, status, using)