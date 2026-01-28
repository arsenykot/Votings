from main.util import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from main.models import *
import json

@check_access(auth = False)
def index_page_view(req):
   return render(req, "index.html")


def login_page_view(req):
    error = getGetOr(req, "error", "")
    uname = getGetOr(req, "username", "")
    goto = getGetOr(req, "next", False)
    return render(req, "account/login.html", {
        "username": uname,
        "error": error,
        "next": goto
    })


@login_required(login_url="/account/login?error=new")
def new_voting_view(req):
    return render(req, "votings/new.html", {})

def register_page_view(req):
    uname = getGetOr(req, "username", "")
    goto = getGetOr(req, "next", False)
    return render(req, "account/register.html", {
        "username": uname,
        "next": goto
    })

@check_access()
def profile_page_view(req):
    user_votings = Voting.objects.filter(author=req.user, taken_down=False).order_by('-date_created')
    return render(req, "account/profile.html", {
        "user_votings": user_votings
    })

@check_access(auth=False)
def existing_voting_view(req, id:int):
    voting = Voting.objects.filter(id=id)
    if len(voting) <= 0:
        return render(req, "votings/error/not_found.html", status=404)
    voting = voting[0]
    if voting.taken_down:
        return render(req, "votings/error/removed.html", status=403)
    if voting.date_closed:
        closing_time = voting.date_closed.ctime()
    else:
        closing_time = False
    checked = []
    voted = False
    if req.user.is_authenticated:
        vote = Vote.objects.filter(user=req.user, voting=voting)
        voted = len(vote) > 0
        if voted:
            checked = vote[0].choice
    options = []
    for i in range(len(voting.options)):
        options.append((i, voting.options[i], i in checked))
    return render(req, "votings/view.html", {
        "title": voting.name,
        "description": voting.description,
        "options": options,
        "multichoice": voting.multichoice,
        "author": voting.author,
        "id": id,
        "closed": voting.closed,
        "closing_time": closing_time,
        "voted": voted
    })

def tos_page_view(req):
    return render(req, "tos.html")

def test_page_view(req):
    checkvars_tests = [
        ["Length min ok test",[str, "abcdef", 6], True],
        ["Length max ok test",[str, "abcdef", 0, 6], True],
        ["Length min bad test",[str, "abcdef", 7], False],
        ["Length max bad test",[str, "abcdef", 0, 5], False],
        ["Length inbetween test",[str, "Lorem ipsum dolor sit amet", 0, 128], True],
        ["Int min ok test", [int, 100, 100], True],
        ["Int max ok test", [int, 100, 0, 100], True],
        ["Int min bad test", [int, 99, 100], False],
        ["Int max bad test", [int, 101, 0, 100], False],
        ["Int inbetween test", [int, 50, 0, 100], True],
        ["Float min ok test", [float, 1.23, 1.00], True],
        ["Float max ok test", [float, 1.23, 0, 1.23], True],
        ["Float min bad test", [float, 0.99, 1.00], False],
        ["Float max bad test", [float, 1.01, 0, 1.00], False],
        ["Float inbetween test", [float, 0.50, 0, 1.00], True],
        ["String regex ok test", [str, "qwerty123", 4, 24, USERNAME_RE_MATCH], True],
        ["String regex bad1 test", [str, "QweRty123", 4, 24, USERNAME_RE_MATCH], False],
        ["String regex bad2 test", [str, "qwerty***", 4, 24, USERNAME_RE_MATCH], False],
        ["String in list ok test", [["foo","bar"], "foo"], True],
        ["String in list bad test", [["foo", "bar"], "baz"], False],
        ["Int in list ok test", [[1, 2, 3], 1], True],
        ["Int in list bad test", [[1, 2, 3], 4], False],
        ["Float in list ok test", [[1.23, 4.56], 1.23], True],
        ["Float in list bad test", [[1.23, 4.56], 7.89], False],
        ["StrInt ok test",[int, "1", 0, 100], True],
        ["StrInt bad test", [int, "1000", 0, 100], False],
        ["StrFloat ok test", [float, "1.23", 0, 1.23], True],
        ["StrFloat bad test", [float, "4.56", 0, 1.23], False],
        ["StrInt in list ok test", [[1, 2, 3], "1"], True],
        ["StrInt in list bad test", [[1, 2, 3], "4"], False],
        ["StrFloat in list ok test", [[1.23, 4.56], "1.23"],True],
        ["StrFloat in list bad test", [[1.23, 4.56], "7.89"], False]
    ]
    for test in checkvars_tests:
        test[1] = (checkVars([test[1]]) == test[2])
    b64_tests = [
        ["base64 encode decode small test", b64dec(b64enc("qwerty")) == "qwerty"],
        ["base64 encode decode big test", b64dec(b64enc(LOREM_IPSUM)) == LOREM_IPSUM],
        ["base64 encode small test", b64enc("qwerty") == "cXdlcnR5"],
        ["base64 encode big test", b64enc(LOREM_IPSUM) == LOREM_IPSUM_B64]
    ]
    return render(req, "test.html", {"checkvars_tests": checkvars_tests, "base64_tests":b64_tests})

@check_access()
def account_settings_view(req):
    return render(req, "account/settings.html", {})

@check_access()
def account_sessions_view(req):
    return render(req, "account/sessions.html", {})

@login_required()
def ban_page_view(req):
    return render(req, "account/banned.html")

@check_access()
def voting_edit(req, id: int):
    voting = Voting.objects.filter(id=id)
    if len(voting) <= 0:
        return render(req, "votings/error/not_found.html", status=404)

    voting = voting[0]

    return render(req, "votings/edit.html", {
        "voting": voting,
        "options": b64enc(json.dumps(voting.options))
    })

def integrity_error_view(req):
    return render(req, "integrity.html")
