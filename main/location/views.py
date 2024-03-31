from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from .models import RepairShop
import csv
import os


def index(request):
    shops = list(RepairShop.objects.values("latitude", "longitude"))
    # print(shops[:2])
    return render(request, "location/index.html", {"shops": shops})


def nearest_shops(request):
    address = request.GET.get("address")
    geolocator = Nominatim(user_agent="main")
    location = geolocator.geocode(address)
    print(location)
    if location:
        user_location = location.latitude, location.longitude
        nearest_shops = []
        shop_distances = {}

        # calculate distances for all shops
        for shop in RepairShop.objects.all():
            shop_location = shop.latitude, shop.longitude
            distance = geodesic(user_location, shop_location).km
            shop_distances[shop] = distance

        sorted_shops = sorted(shop_distances.items(), key=lambda x: x[1])
        for shop, distance in sorted_shops[:5]:
            nearest_shops.append({"shop": shop, "distance": round(distance, 2)})

        return render(
            request,
            "location/index.html",
            {
                "location": location,
                "nearest_shops": nearest_shops,
            },
        )
    else:
        return render(request, "location/index.html", {"error": "Location not found"})


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
    return render(
        request,
        "location/index.html",
        {"message": "CSV file has been saved to your project's data directory."},
    )


download_csv.short_description = "Download selected as csv"


def my_view(request):
    if not request.user.has_perm("You do not have access to download data"):
        return render(
            request,
            "location/index.html",
            {"message": "You do not have permission to download data."},
        )
