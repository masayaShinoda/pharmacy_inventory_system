from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("settings", views.settings, name="settings"),
    path("settings/<str:preference_key>/<str:preference_value>", views.settings, name="settings"),
    path("inventory", views.inventory_view, name="inventory"),
    path("add-pharmacy", views.add_pharmacy_view, name="add_pharmacy"),
    path("clicked", views.clicked, name="clicked"),
]
