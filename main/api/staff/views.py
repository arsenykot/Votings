from django.http import HttpResponse
from main.util import *
from main.models import *
import json
from datetime import date as dateobj, time as timeobj, datetime as dtobj, timezone
from zoneinfo import ZoneInfo
from string import ascii_letters
from random import randint
from django.contrib.auth import login

@check_access(redir=False)
def takedown(req, id):
    if not req.user.is_staff:
        return respond(403, "FORBIDDEN")
    voting = Voting.objects.filter(id=id)
    if len(voting) < 1:
        return respond(404, "NOTFOUND")
    voting = voting[0]
    voting.taken_down = True
    voting.save()
    return redirect("/votings/view/"+str(id))

@check_access(redir=False)
def banuser(req, id):
    if not req.user.is_staff:
        return respond(403, "FORBIDDEN")
    user = User.objects.filter(id=id)
    if len(user) < 1:
        return respond(404, "NOTFOUND")
    user = user[0]
    if req.user.id == user.id:
        return respond(403, "SELFBAN")
    for voting in Voting.objects.filter(author=user):
        voting.taken_down = True
        voting.save()
    user.is_banned = True
    user.save()
    return respond(200, "OK")

@check_access(redir=False)
def unbanuser(req, id):
    if not req.user.is_staff:
        return respond(403, "FORBIDDEN")
    user = User.objects.filter(id=id)
    if len(user) < 1:
        return respond(404, "NOTFOUND")
    user = user[0]
    user.is_banned = False
    user.save()
    return respond(200, "OK")

@check_access(redir=False)
def users(req):
    if not req.user.is_staff:
        return respond(403, "FORBIDDEN")
    show_banned = getPostOr(req, "banned", False) == "on"
    show_staff = getPostOr(req, "staff", False) == "on"

    ret = []
    for user in User.objects.all():
        if not ((not user.is_banned) or (user.is_banned and show_banned)):
            continue
        if not ((not user.is_staff) or (user.is_staff and show_staff)):
            continue
        ret.append(
            {
                "name": user.username,
                "id": user.id,
                "banned": user.is_banned,
                "staff": user.is_staff,
                "votings": len(Voting.objects.filter(author=user))
            }
        )
    return respond(200, json.dumps(ret))
