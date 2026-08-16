from django.urls import path
from .views import (
    register_page,
    login_page,
    logout_page,
    profile_page,
)

urlpatterns = [
    path(
        "login/",
        login_page,
        name="login-page"
    ),
    path(
        "register/",
        register_page,
        name="register-page"
    ),
    path(
        "logout/",
        logout_page,
        name="logout-page"
    ),
    path(
        "profile/",
        profile_page,
        name="profile-page"
    ),
]