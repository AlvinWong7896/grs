from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from .models import RepairShop
import json
import requests
import csv
import os


def index(request):
    shops = list(RepairShop.objects.values("latitude", "longitude"))
    return render(request, "location/index.html", {"shops": shops})


def nearest_shops(request):
    address = request.GET.get("address")
    geolocator = Nominatim(user_agent="main")
    location = geolocator.geocode(address)
    if location:
        user_location = location.latitude, location.longitude
        shop_distances = {}
        for shop in RepairShop.objects.all():
            shop_location = shop.latitude, shop.longitude

            #  calculate the distance between the user location and the shop
            distance = geodesic(user_location, shop_location).km
            shop_distances[distance] = shop_location

        min_distance = min(shop_distances)
        shop_coords = shop_distances[min_distance]
        return JsonResponse(
            {
                "My location": user_location,
                "coordinate": shop_coords,
                "distance": min_distance,
            }
        )
    else:
        return JsonResponse({"Error": "Location not found"})


def download_csv(modeladmin, request, queryset):
    if not request.user.is_staff:
        raise PermissionDenied
    opts = queryset.model._meta
    relative_path = "data"
    base_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_directory, relative_path, "Repair_Shops.csv")
    with open(file_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        field_names = [field.name for field in opts.fields]
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
    # Optionally return a response
    return HttpResponse("CSV file has been saved to the directory.")


download_csv.short_description = "Download selected as csv"


def my_view(request):
    if not request.user.has_perm("You do not have access to download data"):
        raise PermissionDenied

    queryset = RepairShop.objects.all()
    response = download_csv(None, request, queryset)
    return response


# def index(request):
#     if request.method == "POST":
#         pass
#     shops = RepairShop.objects.all()
#     return render(request, "location/index.html", {"shops": shops})


# def location(request):
#     res = requests.get("http://ip-api.com/json/101.127.55.205")
#     location_data = res.text
#     location_data_dict = json.loads(location_data)
#     return render(request, "location/location.html", {"data": location_data_dict})
