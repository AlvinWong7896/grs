from django.shortcuts import render
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from .models import RepairShop
from item.models import Item
import time


def index(request):
    latest_items = Item.objects.filter(is_sold=False).order_by("-created_on")[0:10]
    shops = list(RepairShop.objects.values("latitude", "longitude"))
    return render(
        request, "location/index.html", {"shops": shops, "latest_items": latest_items}
    )


def get_location(geolocator, address, retries=3, delay=1):
    for i in range(retries):
        try:
            return geolocator.geocode(address + ", Singapore")
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            if i < retries - 1:  # If not the last retry, wait and retry
                time.sleep(delay)
            else:  # If the last retry, raise the exception
                raise e


def nearest_shops(request):
    latest_items = Item.objects.filter(is_sold=False).order_by("-created_on")[0:10]
    address = request.GET.get("address")
    geolocator = Nominatim(user_agent="main")
    try:
        location = geolocator.geocode(address + ", Singapore")
    except (GeocoderTimedOut, GeocoderUnavailable):
        return render(
            request,
            "location/index.html",
            {
                "error": "Location service is currently unavailable. Please try again later.",
                "latest_items": latest_items,
            },
        )

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
                "latest_items": latest_items,
            },
        )
    else:
        return render(request, "location/index.html", {"error": "Location not found"})
