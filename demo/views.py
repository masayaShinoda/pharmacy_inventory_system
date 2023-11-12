from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, AddPharmacyForm
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
    try:
        user_preferences = UserPreference.get_user_preferences(user)
    except:
        user_preferences = None

    context = {
        'user_preferences': user_preferences,
    }

    if request.method == "GET":
        return render(request, "settings.html", context)

    if request.method == "PUT":
        print("preference_key", preference_key, " preference_value", preference_value)

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

    # check query param for selected pharmacy
    pharmacy_param = request.GET.get("pharmacy")

    drugs = None
    if pharmacy_param:
        drugs = Pharmacy.filter_pharmacy_drugs(user, pharmacy_param)

    forms = {
        'add_pharmacy': AddPharmacyForm()
    }

    context = {
        'pharmacies': pharmacies,
        'drugs': drugs if drugs else None,
        'forms': forms
    }

    return render(request, "inventory.html", context)

@login_required
@require_http_methods(['POST'])
def add_pharmacy_view(request):
    user = request.user.id

    form = AddPharmacyForm(request.POST)

    if form.is_valid():
        pharmacy_name = form.cleaned_data["name"]
        print(pharmacy_name)
        return HttpResponse(f"""
            <div class="inline-flex items-center gap-2 py-3 px-4 rounded bg-neutral-100 dark:bg-neutral-700 shadow-md">
                <svg
                    class="fill-neutral-700 dark:fill-neutral-100" 
                    xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        width="24"
                        height="24">
                    <path d="M12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12C22 17.5228 17.5228 22 12 22ZM12 20C16.4183 20 20 16.4183 20 12C20 7.58172 16.4183 4 12 4C7.58172 4 4 7.58172 4 12C4 16.4183 7.58172 20 12 20ZM11 7H13V9H11V7ZM11 11H13V17H11V11Z">
                    </path>
                </svg>
                <p id={{ alert_id|default:"" }} class="py-2 px-1">Added new pharmacy: {pharmacy_name}</p>
                <button aria-label="Hide alert message" onclick="this.parentElement.style.display = 'none';">
                    <svg class="fill-neutral-600 dark:fill-neutral-300"
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 24 24"
                            width="24"
                            height="24">
                        <path d="M12.0007 10.5865L16.9504 5.63672L18.3646 7.05093L13.4149 12.0007L18.3646 16.9504L16.9504 18.3646L12.0007 13.4149L7.05093 18.3646L5.63672 16.9504L10.5865 12.0007L5.63672 7.05093L7.05093 5.63672L12.0007 10.5865Z">
                        </path>
                    </svg>
                </button>
            </div>
        """)


@require_http_methods(['POST'])
def clicked(request):
    return HttpResponse("<p>Server has received the click!</p>")
