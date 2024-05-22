from django.urls import path
from . import views

app_name = "location"
urlpatterns = [
    path("", views.index, name="repair_shops"),
    path("nearest_shops/", views.nearest_shops, name="nearest_shops"),
]
