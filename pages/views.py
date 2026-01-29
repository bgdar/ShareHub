from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from django.http import HttpRequest

# Create your views here.

# ---- Pages ---


def dashboard(request: HttpRequest):
    """HALAMAN UTAMA"""
    context = {"title": "dahsboard"}
    return render(request, "pages/dashboard.html", context=context)


# @login_required(login_url=reverse_lazy('accounts_login')) #penamaan
# jika di belum login arahkan ke sini
@login_required(login_url="/accounts/login/")  # lansung url
def home(request: HttpRequest):
    context = {"title": "Home"}
    return render(request, "pages/home.html", context=context)


def about(request: HttpRequest):
    return HttpResponse("about page")


# ---- file -----
@login_required(login_url="accounts:accounts_login")
def upload_file(request: HttpRequest):
    return render(request, "file/upload-file.html")


@login_required(login_url="accounts:accounts_login")
def katagory_file(request: HttpRequest):
    return render(request, "file/file-katagory.html")


@login_required(login_url="accounts:accounts_login")
def history_file(request: HttpRequest):
    return render(request, "file/file-history.html")


def page_not_found_view(request: HttpRequest, exception=None):
    """views yg hanya di jalanakn ketika url (semuanya) tidak ditemukan"""
    return render(request, "404.html", status=404)
