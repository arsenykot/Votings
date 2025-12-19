from django.contrib import admin
from django.urls import path, include
from votings.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("votings.api.urls")),
    path('', index_page_view)
]
