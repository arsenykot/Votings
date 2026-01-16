from django.contrib import admin
from django.urls import path, include
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("main.api.urls")),
    path('', index_page_view),
    path('tos', tos_page_view),
    path('test', test_page_view),
    path('account/login', login_page_view),
    path('votings/new', new_voting_view),
#    path('votings/list', voting_list_view),
    path('votings/view/<int:id>', existing_voting_view),
    path('account/register', register_page_view),
    path('account/profile', profile_page_view)
]
