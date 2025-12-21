from django.contrib import admin
from django.urls import path, include
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("main.api.urls")),
    path('', index_page_view),
    path('account/login', login_page_view),
    path('account/register', register_page_view)
]
