from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "hub/index.html")


def upload(request):
    return HttpResponse("tets upload", content_type="text/html")
# Create your views here.
