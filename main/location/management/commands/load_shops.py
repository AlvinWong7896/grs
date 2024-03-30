from django.conf import settings
from django.core.management.base import BaseCommand
from location.models import RepairShop
import csv


class Command(BaseCommand):
    help = "Load data from Repair Shops file"

    def handle(self, *args, **kwargs):
        data_file = settings.BASE_DIR / "data" / "Repair_Shops.csv"
        keys = ("name", "latitude", "longitude")

        records = []
        with open(data_file, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                records.append({k: row[k] for k in keys})
