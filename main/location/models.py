from django.db import models


class RepairShop(models.Model):
    name = models.CharField(max_length=150)
    address = models.TextField()
    contactName = models.CharField(max_length=150, blank=True)
    phoneNumber = models.CharField(max_length=12, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name
