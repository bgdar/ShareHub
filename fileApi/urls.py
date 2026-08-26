from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("file/upload/", views.upload_file, name="file_api_upload_file"),
    path("file/list/", views.list_files, name="file_api_list_files"),
    path("file/download/<int:file_id>/",
         views.download_file, name="file_api_download_file"),
    path("file/delete/<int:pk>/", views.delete_file, name="file_api_delete_file"),
    # untuk mengambil data file berdasarkan kategory tertentu
    path("file/selected/<str:type_selected>/", views.selected_file,
         name="file_api_selected_file"),

]

# untuk sekaranag aizinkan media bisa di akses memlalui URL , untuk di tampilin di
# 1. detail
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
