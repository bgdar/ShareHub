"""
URL configuration for ShareHub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


import os
from django.urls import path, include, re_path
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.http import FileResponse, Http404
from pages.views import page_not_found_view


def serve_media(request, path):
    """
    Fungsi alternatif untuk membaca file media langsung dari folder 
    dan mengirimkannya ke browser tanpa lewat static() bawaan Django.
    """
    # Gabungkan path folder media dengan nama file yang diminta
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    # Cek apakah file benar-benar ada di komputer
    if os.path.exists(file_path):
        # Kirim file langsung ke browser (Django otomatis membaca tipe konten seperti .webp)
        return FileResponse(open(file_path, 'rb'))

    # Jika tidak ketemu, lempar error 404 standar
    raise Http404("File media tidak ditemukan pada jalur sistem.")


# Django membaca urlpatterns dari atas ke bawah.
urlpatterns = [
    path("", include("pages.urls")),  # halaman "/"
    path("admin/", admin.site.urls),
    path("hub/", include("hub.urls")),
    # url users
    path("accounts/", include("accounts.urls")),  # semua URL auth di sini
    # api utama project
    path("fileApi/", include("fileApi.urls")),



    re_path(r'^media/(?P<path>.*)$', serve_media, name='manual_media'),

]
# custom 404
handler404 = page_not_found_view


# sudah di tangani oleh   fungsion di atas
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL,
#                           document_root=settings.STATIC_ROOT)
