from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm  # form bawaan Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Register user baru


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)   # pakai form bawaan
        if form.is_valid():
            form.save()  # simpan user ke database
            return redirect("accounts:login")  # setelah register → login
    else:
        form = UserCreationForm()  # tampilkan form kosong

    return render(request, "accounts/register.html", {"form": form})

# Dashboard hanya untuk user login

# jika tidak login akan di arahkan ke halamam login


@login_required(login_url="accounts:login")
def dashboard_view(request):
    return render(request, "accounts/dashboard.html", {"user": request.user})
