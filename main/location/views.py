from django.shortcuts import render
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from .models import RepairShop
from item.models import Item


def index(request):
    latest_items = Item.objects.filter(is_sold=False).order_by("-created_on")[0:10]
    shops = list(RepairShop.objects.values("latitude", "longitude"))
    # print(shops[:2])
    return render(
        request, "location/index.html", {"shops": shops, "latest_items": latest_items}
    )


def nearest_shops(request):
    latest_items = Item.objects.filter(is_sold=False).order_by("-created_on")[0:10]
    address = request.GET.get("address")
    geolocator = Nominatim(user_agent="main")
    location = geolocator.geocode(address + ", Singapore")
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
                "latest_items": latest_items,
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
