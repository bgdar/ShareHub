from django.urls import path
from . import views

urlpatterns = [
    path("", views.hub, name="hub"),
    # api untuk hanler message
    path("api/hub/upload/", views.hub_upload, name="api_hub_upload"),
]
