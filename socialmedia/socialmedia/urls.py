
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include("user.urls")),
    path('fr/', include("connection.urls")),
]