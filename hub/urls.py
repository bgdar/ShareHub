from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="hub_index"),
    path("upload/", views.upload, name="hub_upload")
]
