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
        Category, related_name="items", on_delete=models.CASCADE, default="Bike"
    )
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="item_images", blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name="items", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=True)

    # New fields added
    category = models.ForeignKey(
        Category, related_name="items", on_delete=models.CASCADE
    )

    material = models.CharField(
        max_length=22,
        choices=[
            ("Steel", "Steel"),
            ("Aluminum/Foldable Bike", "Aluminum/Alloy"),
            ("Carbon City Bike", "Carbon Fiber"),
            ("Titanium", "Titanium"),
        ],
        blank=True,
        null=True,
    )

    frame_size = models.CharField(
        max_length=5,
        choices=[
            ("XS", "17in"),
            ("S", "17-19in"),
            ("M", "19-22in"),
            ("L", "21-23in"),
            ("XL", ">23in"),
        ],
        blank=True,
        null=True,
    )

    tire_size = models.CharField(
        max_length=8,
        choices=[
            ("10in", "10in"),
            ("12in", "12in"),
            ("14in", "14in"),
            ("16in", "16in"),
            ("20in", "20in"),
            ("22in", "22in"),
            ("24in", "24in"),
            ("26in", "26in"),
            ("27.5in", "27.5in"),
        ],
        blank=True,
        null=True,
    )

    brake_type = models.CharField(
        max_length=25,
        choices=[
            ("Caliper", "Caliper"),
            ("V-Brake", "V-Brake"),
            ("Cantilever", "Cantilever"),
            ("Mechanical Disc", "Mechanical Disc"),
            ("Hydraulic Disc", "Hydraulic Disc"),
        ],
        blank=True,
        null=True,
    )

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
