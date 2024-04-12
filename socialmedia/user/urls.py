from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView)
urlpatterns = [
    path("", views.CustomUserView.as_view()),
    path('<int:pk>/', views.CustomUserView.as_view()),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="login"),
    # path("logout_user/", views.logout_user, name="logout_user"),
    path("register/", views.user_register_view, name="register"),

]