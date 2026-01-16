from django.http import HttpResponse
from main.util import *
from main.models import *
import json
from datetime import date as dateobj, time as timeobj, datetime as dtobj

def test_api_view(req):
    return HttpResponse(json.dumps({"POST": req.POST, "GET": req.GET}, indent=2, ensure_ascii=False))

def voting_new_view(req):
    if not req.user.is_authenticated:
        return respond(401, "UNAUTHORIZED")
    name = getPostOr(req, "name", False)
    desc = getPostOr(req, "description", "")
    option1 = getPostOr(req, "option1", False)
    option2 = getPostOr(req, "option2", False)
    close = getPostOr(req, "close", False)
    date = getPostOr(req, "date", False)
    time = getPostOr(req, "time", False)

    if False in [name, option1, option2, close]:
        return respond(400, "BADREQUEST")
    
    if not checkVars([
        [str, name, 1, 48],
        [str, desc, 0, 512],
        [str, option1, 1, 48],
        [str, option2, 0, 48],
        [["auto", "manual"], close]
    ]):
        return respond(400, "BADREQUEST")
    
    if close == "auto" and False in [date, time]:
        return respond(400, "BADREQUEST")
    datetime = None
    if close == "auto":
        try:
            date = dateobj.fromisoformat(date)
            time = timeobj.fromisoformat(time)
            datetime = dtobj.combine(date, time)
        except ValueError:
            return respond(400, "BADDATE")
    
    voting = Voting(author=req.user, name=name, description=desc, option1=option1, option2=option2, date_closed=datetime)
    voting.save()
    return HttpResponse("OK")
