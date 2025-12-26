from django.urls import path, include
from main.api.views import *

urlpatterns = [
    path('auth/', include("main.api.auth.urls")),
    path('registration/', include("main.api.registration.urls")),
    path("test", test_api_view)
]
