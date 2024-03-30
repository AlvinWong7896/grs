from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from .models import RepairShop
import json
import requests
import csv


def index(request):
    shops = list(RepairShop.objects.values("latitude", "longitude"))
    print(shops[:2])
    return render(request, "location/index.html", {"shops": shops})


def download_csv(modeladmin, request, queryset):
    if not request.user.is_staff:
        raise PermissionDenied
    opts = queryset.model._meta
    model = queryset.model
    response = HttpResponse(content_type="text/csv")
    # force download
    response["Content-Disposition"] = "attachment;filename=export.csv"
    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response


download_csv.shortdescription = "Download selected as csv"


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
