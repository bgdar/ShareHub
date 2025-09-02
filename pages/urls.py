from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="page_dashboard"),
    path("home/", views.home, name="page_home"),
    path("about/", views.about, name="page_about"),
]
