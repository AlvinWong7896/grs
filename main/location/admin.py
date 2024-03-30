from django.contrib import admin
from .models import RepairShop


@admin.register(RepairShop)
class RepairShopAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "address",
        "contactName",
        "phoneNumber",
        "latitude",
        "longitude",
    )
    search_fields = ["name", "address"]
