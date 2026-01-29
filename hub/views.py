from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.core.serializers import serialize

from .models import hubs


@login_required(login_url="accounts:accounts_login")
def hub(request: HttpRequest):
    """Halaman utama"""
    user = request.user
    data_hub = serialize("json", hubs.objects.select_related("user"))

    return render(
        request, "hub/hub.html", context={"user ": user, "data_hub": data_hub}
    )


# @login_required(login_url="accounts:accounts_login")
# def upload(request: HttpRequest):
#     if request.method == "GET":
#         return render(request, "hub/upload.html")


# -----API --------
@login_required(login_url="accounts:accounts_login")
def hub_upload(request: HttpRequest):
    """upload , update message dari hub.html"""
    user = request.user
    if request.method == "POST":
        # update message
        message = request.POST.get("message")
        path_file = request.POST.get("mess")
        # dapatkan dari api yang di kirim kembali yang di kirm
        path_file = request.POST.get("file_path")
        hubs.objects.create(
            message=message,
            file_path=path_file,
            user=user,
        )
        messages.info(request, message="Message Updated")
        return redirect("hub")


def page_not_found(request: HttpRequest):
    render(request=request, template_name="404.html")
