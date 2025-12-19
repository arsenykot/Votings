from django.urls import path, include
from main.api.views import *

urlpatterns = [
    path('test', test_api_view),
    path('login', auth_login_view),
    path('logout', auth_logout_view)
]
