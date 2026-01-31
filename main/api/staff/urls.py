from django.urls import path, include
from main.api.staff.views import *

urlpatterns = [
    path('takedown/<int:id>', takedown),
    path('ban/<int:id>', banuser),
    path('unban/<int:id>', unbanuser),
    path('users', users)
]
