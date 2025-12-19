from django.urls import path, include
from main.api.views import *

urlpatterns = [
    path('test', test_api_view)
]
