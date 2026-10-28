
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .admin_views import admin_tools

urlpatterns = [
    path("register/", views.register, name="register"),

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html",
            redirect_authenticated_user=True
        ),
        name="login"
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),
    path("admin-tools/", admin_tools, name="admin_tools"),
]
