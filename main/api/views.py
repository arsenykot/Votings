from django.http import HttpResponse
from main.util import *
from main.models import *
import json
from datetime import date as dateobj, time as timeobj, datetime as dtobj, timezone
from zoneinfo import ZoneInfo
from string import ascii_letters
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

#Под удаление перед релизом
def test_search_view(req):
    user1 = User(username=rstr(16))
    user2 = User(username=rstr(16))
    user1.save()
    user2.save()
    SAMPLE_VOTINGS = [
        [
            "Lorem Ipsum",
            LOREM_IPSUM,
            ["Option A", "Option B"],
            False,
            ["2026-01-01 12:34", "2026-01-31 23:59"],
            user2
        ],
        [
            "Locked voting",
            "You will not be able to vote here",
            ["Option A", "Option B"],
            True,
            ["1970-01-01 12:34", "1970-01-31 23:59"],
            user2
        ],
        [
            "Best keyboard layout",
            "Which keyboard layout is better?",
            ["QWERTY", "Dvorak", "Colemak"],
            False,
            ["2026-01-01 12:34", "2026-01-31 23:59"],
            user1
        ],
        [
            "Test voting 123",
            LOREM_IPSUM,
            ["Option A", "Option B"],
            False,
            ["2026-01-01 12:34", "2026-01-31 23:59"]
        ]
    ]
    for i in range(32):
        k = user2
        if i %4 == 0:
            k = user1
        SAMPLE_VOTINGS.append([
            "Lorem Ipsum "+str(i),
            LOREM_IPSUM,
            ["Option A", "Option B"],
            False,
            ["2026-01-01 12:34", "2026-01-31 23:59"],
             k
        ])
    for voting in SAMPLE_VOTINGS:
        u = req.user
        if len(voting) > 5:
            u = voting[5]
        times = voting[4]
        stime = dtobj.fromisoformat(times[0])
        etime = None
        if len(times) > 1:
            etime = dtobj.fromisoformat(times[1])
        vobj = Voting(author=u, name=voting[0], description=voting[1], options=voting[2], multichoice=voting[3], date_created = stime, date_closed = etime)
        vobj.save()
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
    choice = getPostOr(req, "choice", False)
    if choice == False:
        return respond(400,"BADREQUEST")
    
    voting = Voting.objects.filter(id=id)
    if len(voting) <= 0:
        return respond(404, "NOTFOUND" )
    voting = voting[0]
    if voting.multichoice:
        try:
            choice = json.loads(b64dec(choice))
            for i,c in enumerate(choice):
                if not checkVars([[int,c,0,len(voting.options)-1]]):
                    return respond(400, "BADREQUEST")
                choice[i] = int(c)
        except:
            return respond(400,"BADREQUEST")
    else:
        if checkVars([
            [int, choice, 0, len(voting.options)]
           ]):
            choice = [int(choice)]
        else:
            return respond(400, "BADREQUEST")
    vote = Vote.objects.filter(user=req.user, voting=voting)
    if len(vote) <= 0:
        vote = Vote(user=req.user, voting=voting, choice=choice)
    else:
        vote = vote[0]
        vote.choice = choice
    vote.save()
    return respond(200, "OK")

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
@check_access(redir=False, auth=False)
def search_view(req):
    q = trisplit(getPostOr(req, "query", "").lower())
    ret = []
    hp = -1
    for voting in Voting.objects.all():
        score = 0
        for word in q:
            score += voting.name.lower().count(word)
            score += voting.description.lower().count(word)
        t = voting.date_created.strftime("%H:%M:%S %d/%m/%Y")
        if voting.date_closed != None:
            t += " - " + voting.date_closed.strftime("%H:%M:%S %d/%m/%Y")
        else:
            t = "Created at " + t
        ret.append((score,{
            "name": voting.name,
            "description": voting.description,
            "id": voting.id,
            "time": t
            }))
        if score > hp:
            hp = score
    ret = sorted(ret, key= lambda part: part[0], reverse = True)
    if hp <= 0 and len(" ".join(q)) > 1:
        return respond(204,"")
    elif hp > 0:
        tmp = list(ret)
        ret = []
        for q in tmp:
            if q[0] >= 1:
                ret.append(q)
    return respond(200,json.dumps(ret))
