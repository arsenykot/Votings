from django.urls import path, include
from main.api.staff.views import *

urlpatterns = [
    path('takedown/<int:id>', takedown),
    path('delreport/<int:id>', remove_report),
    path('ban/<int:id>', banuser),
    path('qban/<int:id>/<int:back>', banuser_quick),
    path('unban/<int:id>', unbanuser),
    path('users', users),
    path('reports', list_reports)
]
