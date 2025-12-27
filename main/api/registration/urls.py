from django.urls import path, include
from main.api.registration.views import *

urlpatterns = [
    path('check_name', name_view),
    path('register', register_view)
]