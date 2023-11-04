from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm
from .models import Manager, UserPreference, Pharmacy, Drug


@login_required
@require_http_methods(["GET"])
def index(request):
    user = request.user.id

    context = {
        'pharmacies': Pharmacy.filter_managed_pharmacies(user),
    }

    return render(request, "index.html", context)


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
                messages.add_message(
                    request, messages.ERROR, "Invalid username or password.")
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
@require_http_methods(["GET", "PUT"])
def settings(request, preference_key=None, preference_value=None):
    user = request.user.id
    context = {
        'user_preferences': UserPreference.get_user_preferences(user),
    }

    if request.method == "GET":
        return render(request, "settings.html", context)

    if request.method == "PUT":
        if preference_key == "preferred-theme":
            if preference_value == "light":
                UserPreference.set_user_preferred_theme(user, "light")
                return render(request, "settings.html", context)
            elif preference_value == "dark":
                UserPreference.set_user_preferred_theme(user, "dark")
                return render(request, "settings.html", context)

    else:
        return HttpResponseBadRequest()

@login_required
@require_http_methods(['GET'])
def inventory_view(request):
    user = request.user.id
    pharmacies = Pharmacy.filter_managed_pharmacies(user)

    pharmacy_param = request.GET.get("pharmacy")
    # selected_pharmacy = Pharmacy.objects.filter(pk=pharmacy_param)

    # TODO: check query param for selected pharmacy
    drugs = None
    if pharmacy_param:
        drugs = Pharmacy.filter_pharmacy_drugs(user, pharmacy_param)

    context = {
        'pharmacies': pharmacies,
        'drugs': drugs if drugs else None
    }

    return render(request, "inventory.html", context)

@require_http_methods(['POST'])
def clicked(request):
    return HttpResponse("<p>Server has received the click!</p>")
