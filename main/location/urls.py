from django.urls import path
from . import views

app_name = "location"
urlpatterns = [
    path("", views.index, name="repair_shops"),
    path("nearest_shop/", views.nearest_shops, name="nearest_shops"),
    path("download-csv/", views.my_view, name="download_csv"),
    # path("", views.location, name="location"),
]
