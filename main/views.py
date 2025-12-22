from main.util import *
from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import HttpResponse

def index_page_view(req):
   return render(req, "index.html")

def login_page_view(req):
    error = getGetOr(req, "error", "")
    uname = getGetOr(req, "username", "")
    return render(req, "account/login.html", {
        "username": uname,
        "error": error
    })

def new_voting_view(req):
    if auth.get_user(req).is_authenticated:
        return HttpResponse("this is new voting page")
    else:
        return redirect("/account/login?error=new")