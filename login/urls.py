from django.urls import path
from .views import login, logout, userinfo

app_name = "loginapp"
urlpatterns = [
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("user/", userinfo, name="user"),
]