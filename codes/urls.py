from django.urls import path
from .views import add_code, view_codes, remove_code, home

urlpatterns = [
    path("", home, name="home"),  # Add this for the homepage

    path("add/", add_code, name="add_code"),
    path("codes/", view_codes, name="view_codes"),
    path("remove/<str:code>/", remove_code, name="remove_code"),
]
