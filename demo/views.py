from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm
from .models import Pharmacy

@login_required
@require_http_methods(["GET"])
def index(request):
    return render(request, "index.html")

@require_http_methods(["GET", "POST"])
def login_view(request):
    form = LoginForm()
    if request.method == "GET":
        return render(request, "login.html", {
            "form": form,
            "layout_options": {
                "sidebar": False,
            }
        })

    elif request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)
        
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                messages.add_message(request, messages.ERROR, "Invalid username or password.")
                return render(request, "login.html", {
                    "form": form,
                    "layout_options": {
                        "sidebar": False,
                    }
                })

@require_http_methods(["GET"])
def logout_view(request):
    logout(request)
    return redirect("index")
    

@login_required
def settings(request):
    user = request.user.id

    context = {
        'pharmacies': Pharmacy.get_managed_pharmacies(user),
    }

    return render(request, "settings.html", context)

@require_http_methods(['POST'])
def clicked(request):
    return HttpResponse("<p>Server has received the click!</p>")