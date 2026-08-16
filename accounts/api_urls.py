from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    ProfileView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
urlpatterns = [
    path(
        "register/",
        RegisterView.as_view(),
        name="register-api"
    ),
    path(
        "login/",
        LoginView.as_view(),
        name="login-api"
    ),
    path(
        "profile/",
        ProfileView.as_view(),
        name="profile-api"
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token-refresh"
    ),
]