from django.urls import path, include
from main.api.auth.views import *

urlpatterns = [
    path('login', login_view),
    path('logout', logout_view)
]