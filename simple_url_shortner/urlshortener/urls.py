from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.urls import path, re_path

from .views import index, redirect, register_user

urlpatterns = [
    path("", index, name="index"),
    re_path(r"^(?P<short_code>[A-Za-z0-9]+)$", redirect, name="redirect"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="login.html",
            extra_context={"user_register_form": UserCreationForm},
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("register/", register_user, name="register"),
]
