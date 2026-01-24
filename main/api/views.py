from django.http import HttpResponse
from main.util import *
from main.models import *
import json
from datetime import date as dateobj, time as timeobj, datetime as dtobj, timezone
from zoneinfo import ZoneInfo
from random import randint
from django.contrib.auth import login


# Под удаление перед релизом
@check_access(redir=False)
def test_api_view(req):
    return HttpResponse(json.dumps({"POST": req.POST, "GET": req.GET}, indent=2, ensure_ascii=False))

# Под удаление перед релизом
@check_access(redir=False)
def ban_self_view(req):
    req.user.is_banned = True
    req.user.save()
    return respond(200, "Goodbye!")

# Под удаление перед релизом
def create_account_quick(req, arg:str):
    u = User(username="u"+str(randint(100000, 999999)))
    u.is_active = True
    if arg in ["staff", "su"]:
        u.is_staff = True
    if arg == "su":
        u.is_superuser = True
    u.set_password("1234567890")
    u.save()
    login(req, u)
    return redirect("/test")

@check_access(redir=False)
def voting_new_view(req):
    name = getPostOr(req, "name", False)
    desc = getPostOr(req, "description", "")
    options = getPostOr(req, "options", False)
    close = getPostOr(req, "close", False)
    date = getPostOr(req, "date", False)
    time = getPostOr(req, "time", False)
    tz = getPostOr(req, "timezone", False)
    multi = getPostOr(req, "multichoice", "off")
    multi = (multi == "on")

    if False in [name, options, close, tz]:
        return respond(400, "BADREQUEST")
    
    if not checkVars([
        [str, name, 1, 48],
        [str, desc, 0, 512],
        [["auto", "manual"], close]
    ]):
        return respond(400, "BADREQUEST")
    try:
        options = b64dec(options)
        options = json.loads(options)
        for option in options:
            if not (1 < len(option) < 48):
                return respond(400, "BADREQUEST")
        if len(options) < 2:
            return respond(400, "TOOFEWOPTIONS")
        elif len(options) > 10:
            return respond(400, "TOOMANYOPTIONS")
    except:
        return respond(400, "BADREQUEST")
    
    if close == "auto" and False in [date, time]:
        return respond(400, "BADREQUEST")
    datetime = None
    if close == "auto":
        try:
            date = dateobj.fromisoformat(date)
            time = timeobj.fromisoformat(time)
            datetime = dtobj.combine(date, time)
            datetime = dtobj.fromtimestamp(datetime.timestamp(), ZoneInfo(str(tz)))
            if datetime.timestamp() < datetime.now().timestamp():
                return respond(400, "DATEINPAST")
        except ValueError:
            return respond(400, "BADDATE")
    
    voting = Voting(author=req.user, name=name, description=desc, options=options, date_closed=datetime, multichoice=(multi!=False))
    voting.save()
    return HttpResponse(str(voting.id))

@check_access(redir=False)
def voting_vote_view(req, id:int):
    pass

@check_access(redir=False)
def voting_edit_view(req, id:int):
    voting = Voting.objects.filter(id=id)
    totalChangedChars = 0 # todo: ограничить максимальное число модификаций
    if len(voting) <= 0:
        return respond(404, "NOTFOUND")
    voting = voting[0]
    
    if req.user != voting.author:
        return respond(403, "FORBIDDEN")
    
    if voting.closed:
        return respond(400, "CLOSED")
    
    name = getPostOr(req, "title", False)
    desc = getPostOr(req, "description", False)
    multichoice = getPostOr(req, "multichoice", False)
    if False in [name, multichoice]:
        return respond(400, "BADREQUEST")
    if not checkVars([
        [str, name, 1, 48],
        [str, desc, 0, 512],
        [["on", "off"], multichoice]
    ]):
        return respond(400, "BADREQUEST")
    voting.name = name
    voting.description = desc
    voting.multichoice = multichoice=="on"

    raw_options = getPostOr(req, "options", False)
    try:
        options = json.loads(b64dec(raw_options))
        for option in options:
            if not 0 < len(option) <= 48:
                return respond("BADREQUEST")
    except:
        return respond(400, "BADREQUEST")

    if len(options) < 2:
        return respond(400, "TOOFEWOPTIONS")
    elif len(options) > 10:
        return respond(400, "TOOMANYOPTIONS")

    voting.options = options
    voting.save()

    return respond(200, "OK")

@check_access(redir=False)
def voting_close_view(req, id:int):
    voting = Voting.objects.filter(id=id)
    if len(voting) <= 0:
        return respond(404, "NOTFOUND")
    voting = voting[0]
    
    if req.user != voting.author:
        return respond(403, "FORBIDDEN")
    
    if voting.closed:
        return respond(400, "CLOSED")
    
    voting.closed = True
    voting.save()

    return respond(200, "OK")