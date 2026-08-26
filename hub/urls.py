from django.urls import path
from . import views
from django.urls import path, include, re_path
from django.conf.urls.static import static
import os
from django.http import Http404


urlpatterns = [
    path("", views.hub, name="hub"),
    # api untuk hanler message
    path("api/upload/", views.hub_message, name="api_hub_message"),
    path('api/hub/add-file/', views.api_add_hud_file, name='api_add_hud_file'),
    path('api/message/', views.api_add_message, name='api_hub_message'),
    path('api/comment/<str:hub_id>/',
         views.api_add_comment, name='api_add_comment'),

    path('api/list/', views.api_hub_list, name='api_hub_list'),

    # spesifikasi file
    path('file/<int:id>/', views.detail_file_view, name='hub_detail_file'),



]
