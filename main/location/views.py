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
    address += ", Singapore"
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
        for shop, distance in sorted_shops[:10]:
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


def my_view(request):
    if not request.user.has_perm("You do not have access to download data"):
        return render(
            request,
            "location/index.html",
            {"message": "You do not have permission to download data."},
        )
