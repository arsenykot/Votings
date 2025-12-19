from django.urls import path, include
from votings.api.views import *

urlpatterns = [
    path('test', test_api_view)
]
