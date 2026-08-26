from django.urls import path

from . import views

# test nama namespace untuk di gunakna di url

urlpatterns = [
    path("", views.dashboard, name="page_dashboard"),
    path("home/", views.home, name="page_home"),
    path("about/", views.about, name="page_about"),
    # ---file ---
    path("file/upload/", views.upload_file, name="page_file_upload"),
    path("file/catagory/", views.katagory_file, name="page_file_katagory"),
    path("file/history", views.history_file, name="page_history_file"),

]
