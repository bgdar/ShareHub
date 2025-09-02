from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
# Create your views here.


def dashboard(request):
    context = {
        "title": "dahsboard"
    }

    return render(request, "pages/dashboard.html", context=context)


# @login_required(login_url=reverse_lazy('accounts_login')) #penamaan
# jika di belum login arahkan ke sini
@login_required(login_url='/accounts/login/')
def home(request):
    context = {
        "title": "Home"
    }
    return render(request, "pages/home.html", context=context)


def about(request):
    return HttpResponse("about page")


def page_not_found_view(request, exception=None):
    '''views yg hanya di jalanakn ketika url (semuanya) tidak ditemukan'''
    return render(request, "404.html", status=404)
