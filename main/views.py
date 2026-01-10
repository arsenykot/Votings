from main.util import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import HttpResponse
from main.models import Voting

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

def profile_page_view(req):
    return render(req, "account/profile.html")

def existing_voting_view(req, id:int):
    voting = Voting.objects.filter(id=id)
    if len(voting) <= 0:
        return render(req, "votings/error/not_found.html", status=404)
    voting = voting[0]
    return render(req, "votings/view.html", {
        "title": voting.name,
        "description": voting.description,
        "options": [(0, voting.option1), (1, voting.option2)], # заглушка
        "author": voting.author
    })