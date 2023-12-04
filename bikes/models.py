from django.db import models


class Appointment(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact_number = models.SmallIntegerField(max_length=8)
    email_addr = models.EmailField()

    def __str__(self):
        return self.first_name + " " + self.last_name


class Bike(models.Model):
    name = (models.CharField(max_length=50),)
    model = (models.CharField(max_length=50),)
    new_price = models.DecimalField(max_digits=8, decimal_places=2)
    selling_price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(max_length=800, default="")

    def __str__(self):
        return self.name
