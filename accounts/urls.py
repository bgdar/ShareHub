from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = "accounts"

urlpatterns = [
    path("register/", views.register_view, name="accounts_register"),
    path("login/", LoginView.as_view(template_name="auth/login.html"),  # sudah menggunakan tempalte jadi gak perlu login manual
         name="accounts_login"),
    path("logout/", LogoutView.as_view(next_page="accounts:login"),
         name="accounts_logout"),
    path("profile/", views.profile_view, name="accounts_profile"),
]
