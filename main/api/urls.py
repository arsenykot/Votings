from django.urls import path, include
from main.api.views import *

urlpatterns = [
    path('test', test_api_view),
    path('ban_self', ban_self_view),
    path('test_user/<str:arg>/', create_account_quick),
    path('test_search', test_search_view),
    path('voting/new', voting_new_view),
    path('voting/edit/<int:id>', voting_edit_view),
    path('voting/close/<int:id>', voting_close_view),
    path('voting/vote/<int:id>', voting_vote_view),
    path('voting/unvote/<int:id>', voting_unvote_view),
    path('voting/report/<int:id>', report_voting),
    path('search', search_view),
    path('settings/theme', settings_theme_view),
    path('settings/password', settings_password_view),
    path('settings/delete', delete_account),
    path('auth/', include("main.api.auth.urls")),
    path('registration/', include("main.api.registration.urls")),
    path('staff/', include("main.api.staff.urls"))
]
