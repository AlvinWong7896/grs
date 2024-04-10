from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("contact/", views.contact, name="contact"),
    path("signupuser/", views.signupuser, name="signupuser"),
    path("loginuser/", views.loginuser, name="loginuser"),
    path("logoutuser/", views.logoutuser, name="logoutuser"),
]
