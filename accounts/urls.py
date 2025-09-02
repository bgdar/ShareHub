from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = "accounts"

urlpatterns = [
    path("register/", views.register_view, name="accounts_register"),
    path("login/", LoginView.as_view(template_name="accounts/login.html"),
         name="accounts_login"),
    path("logout/", LogoutView.as_view(next_page="accounts:login"),
         name="accounts_logout"),
    path("dashboard/", views.dashboard_view, name="accounts_dashboard"),
]
