from django.shortcuts import render

def index_page_view(req):
    return render(req, "index.html")