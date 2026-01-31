from django.urls import path, include
from main.staffportal.views import *

urlpatterns = [
    path("users", users_list),
    path("reports", reports_list)
]