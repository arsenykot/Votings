from hashlib import sha256
from time import time
from main.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from random import choice
from string import ascii_letters
import re
import base64

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

def check_access(auth = True, bans = True, redir = True):
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

def b64dec(b64str):
    fmtstr = '\n'.join(b64str[pos:pos+76] for pos in range(0, len(b64str), 76))
    return base64.decodebytes(bytes(fmtstr, encoding="utf-8")).decode(encoding="utf-8")

def b64enc(rawstr):
    encstr = base64.encodebytes(bytes(rawstr, encoding="utf-8")).decode(encoding="utf-8")
    return encstr.replace("\n","")

def rstr(l):
    ret = ""
    for i in range(l):
        ret += choice(ascii_letters)
    return ret

def trisplit(s):
    if len(s) <= 3:
        return [s]
    ret = []
    for i in range(1, len(s)-2):
        ret.append(s[i-1:i+1])
    return ret

LOREM_IPSUM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent iaculis erat eu libero efficitur, vel ultrices ipsum consequat. Cras finibus tincidunt mi, non eleifend orci."
LOREM_IPSUM_B64 = "TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQsIGNvbnNlY3RldHVyIGFkaXBpc2NpbmcgZWxpdC4gUHJhZXNlbnQgaWFjdWxpcyBlcmF0IGV1IGxpYmVybyBlZmZpY2l0dXIsIHZlbCB1bHRyaWNlcyBpcHN1bSBjb25zZXF1YXQuIENyYXMgZmluaWJ1cyB0aW5jaWR1bnQgbWksIG5vbiBlbGVpZmVuZCBvcmNpLg=="