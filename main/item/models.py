from django.contrib.auth.models import User
from django.db import models
import locale


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Item(models.Model):
    category = models.ForeignKey(
        Category, related_name="items", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="item_images", blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name="items", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def formatted_price(self):
        """
        Returns the formatted price as a strong in xxx,xxx.00 format
        """

        # Set the Locale to the default locale
        locale.setlocale(locale.LC_ALL, "")

        # Format the price using the current locale
        formatted_price = locale.currency(self.price, grouping=True)

        # Reset the locale to the default (usually 'C' or POSIX') to avoid side effects
        locale.setlocale(locale.LC_ALL, "C")

        return formatted_price
