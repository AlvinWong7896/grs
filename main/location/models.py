from django.db import models


class RepairShop(models.Model):
    name = models.CharField(max_length=150)
    address = models.TextField()

    def __str__(self):
        return self.name
