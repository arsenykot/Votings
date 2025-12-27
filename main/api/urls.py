from django.urls import path, include
from main.api.views import *

urlpatterns = [
    path('test', test_api_view),
    path('new', voting_new_view),
    path('auth/', include("main.api.auth.urls")),
    path('registration/', include("main.api.registration.urls"))
]
