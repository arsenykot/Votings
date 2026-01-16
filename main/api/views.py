from django.http import HttpResponse
from main.util import *
from main.models import *
import json
import base64
from datetime import date as dateobj, time as timeobj, datetime as dtobj

@check_auth(redir=False)
def test_api_view(req):
    return HttpResponse(json.dumps({"POST": req.POST, "GET": req.GET}, indent=2, ensure_ascii=False))

@check_auth(redir=False)
def ban_self_view(req):
    req.user.is_banned = True
    req.user.save()
    return respond(200, "Goodbye!")

@check_auth(redir=False)
def voting_new_view(req):
    name = getPostOr(req, "name", False)
    desc = getPostOr(req, "description", "")
    options = getPostOr(req, "options", False)
    close = getPostOr(req, "close", False)
    date = getPostOr(req, "date", False)
    time = getPostOr(req, "time", False)
    multi = getPostOr(req, "multichoice", "off")
    multi = (multi == "on")

    if False in [name, options, close]:
        return respond(400, "BADREQUEST")
    
    if not checkVars([
        [str, name, 1, 48],
        [str, desc, 0, 512],
        [["auto", "manual"], close]
    ]):
        return respond(400, "BADREQUEST")
    try:
        options = base64.decodebytes(bytes(options, encoding="utf-8")).decode(encoding="utf-8")
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
            if datetime.timestamp() < datetime.now().timestamp():
                return respond(400, "DATEINPAST")
        except ValueError:
            return respond(400, "BADDATE")
    
    voting = Voting(author=req.user, name=name, description=desc, options=options, date_closed=datetime, multichoice=(multi!=False))
    voting.save()
    return HttpResponse(str(voting.id))

@check_auth(redir=False)
def voting_vote_view(req, id:int):
    pass