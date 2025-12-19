from django.http import HttpResponse
from main.util import *
from main.models import *
from time import time, sleep

def test_api_view(req):
    return HttpResponse(getSessOr(req, "token", "Unauthorized"))

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
        passwd = saltedHash(passwd, uname)
        cuser = User.objects.filter(username=uname, password=passwd)
        if len(cuser) <= 0:
            text = "BADCREDENTIALS"
            status = 403
        else:
            cuser = cuser.first()
            text = grantNewToken(cuser)
            req.session["token"] = text
            req.session["username"] = uname
    resp = HttpResponse(text)
    resp.status_code = status
    return resp

def auth_logout_view(req):
    req.session["token"] = None
    resp = HttpResponse()
    resp.status_code = 302
    resp.headers["Location"] = "/"
    return resp