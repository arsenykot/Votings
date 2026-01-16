from django.urls import path, include
from main.staffportal.views import *

urlpatterns = [
    path("reports", report_list_view)
]