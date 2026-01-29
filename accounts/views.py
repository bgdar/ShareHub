from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm  # form bawaan Django
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.http import HttpRequest


# Register user baru
def register_view(request: HttpRequest):
    username = request.POST.get("username")
    password = request.POST.get("password")
    if request.method == "POST":
        form = UserCreationForm(request.POST)  # pakai form bawaan
        if form.is_valid():
            form.save()  # simpan user ke database
            # setelah register → login

            messages.info(request, "Silahkan login")
            return redirect("accounts:accounts_login")
        # cek data di database user
        elif User.check(username=username, password=password):
            messages.warning("Nama dan passsword tersebut sudah ada ")
            return redirect("accounts:accounts_login")
        else:
            messages.warning(
                request=request, message="data yang anda masukan tidak valid"
            )
    else:
        messages.info(request, "Register page")
        form = UserCreationForm()  # tampilkan form kosong

    return render(request, "auth/register.html", {"form": form})


# Dashboard hanya untuk user login

# jika tidak login akan di arahkan ke halamam login


@login_required(login_url="accounts:accounts_login")
def profile_view(request):

    context = {
        "skill": " Django,Python,TailwindCSS,Alpine.js,PostgreSQL,Docker".split(),
        "user": request.user,
    }

    return render(request, "page/profile.html", context=context)
