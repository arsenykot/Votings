from django.urls import path, include
from main.api.views import *

urlpatterns = [
    path('test', test_api_view),
    path('ban_self', ban_self_view),
    path('test_user/<str:arg>/', create_account_quick),
    path('new', voting_new_view),
    path('auth/', include("main.api.auth.urls")),
    path('registration/', include("main.api.registration.urls"))
]
