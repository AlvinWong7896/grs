from django.shortcuts import render
import json
import requests


def location(request):
    res = requests.get("http://ip-api.com/json/101.127.55.205")
    location_data = res.text
    location_data_dict = json.loads(location_data)
    return render(request, "location/location.html", {"data": location_data_dict})
