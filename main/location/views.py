from django.shortcuts import render, get_object_or_404
from .models import RepairShop
import json
import requests


def index(request):
    if request.method == "POST":
        pass
    shops = RepairShop.objects.all()
    return render(request, "location/index.html", {"shops": shops})


# def location(request):
#     res = requests.get("http://ip-api.com/json/101.127.55.205")
#     location_data = res.text
#     location_data_dict = json.loads(location_data)
#     return render(request, "location/location.html", {"data": location_data_dict})
