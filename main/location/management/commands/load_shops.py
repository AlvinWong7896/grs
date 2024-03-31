import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from location.models import RepairShop


class Command(BaseCommand):
    help = "Load data from Repair Shop file"

    def handle(self, *args, **kwargs):
        data_file = settings.BASE_DIR / "data" / "Repair_Shops.csv"
        keys = (
            "name",
            "address",
            "contactName",
            "phoneNumber",
            "latitude",
            "longitude",
        )  # the CSV columns we will gather data from.

        records = []
        with open(data_file, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                records.append({k: row[k] for k in keys})

        # extract the latitude and longitude from the Point object
        for record in records:
            # add the data to the database
            RepairShop.objects.get_or_create(
                name=record["name"],
                address=record["address"],
                contactName=record["contactName"],
                phoneNumber=record["phoneNumber"],
                latitude=record["latitude"],
                longitude=record["longitude"],
            )
