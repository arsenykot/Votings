from main.util import *

def index_page_view(req):
    return render(req, "index.html")

def login_page_view(req):
    uname = getGetOr(req, "username", "")
    return render(req, "account/login.html", {
        "username": uname
    })