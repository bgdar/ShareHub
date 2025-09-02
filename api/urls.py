from django.urls import path
from . import views


urlpatterns = [
    path("file/upload/", views.upload_file, name="upload_file"),
    path("file/list/", views.list_files, name="list_files"),
    path("file/download/<int:file_id>/",
         views.download_file, name="download_file"),
    path("file/delete/<int:pk>/", views.delete_file, name="delete_file"),
]
