from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image
import locale, os, tempfile

# from tinymce.models import HTMLField


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
    name = models.CharField(max_length=50)
    # description = HTMLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="item_images", blank=True, null=True)
    image_2 = models.ImageField(upload_to="item_images", blank=True, null=True)
    image_3 = models.ImageField(upload_to="item_images", blank=True, null=True)
    image_4 = models.ImageField(upload_to="item_images", blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name="items", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=True)
    material = models.CharField(
        max_length=22,
        choices=[
            ("Steel", "Steel"),
            ("Aluminum/Alloy", "Aluminum/Alloy"),
            ("Carbon Fiber", "Carbon Fiber"),
            ("Titanium", "Titanium"),
        ],
        blank=True,
        null=True,
    )

    drivetrain = models.CharField(
        max_length=9,
        choices=[
            ("Nil", "Nil"),
            ("7-speed", "7-speed"),
            ("8-speed", "8-speed"),
            ("9-speed", "9-speed"),
            ("10-speed", "10-speed"),
            ("11-speed", "11-speed"),
            ("12-speed", "12-speed"),
            (">12-speed", ">12-speed"),
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
            ("18in", "18in"),
            ("20in", "20in"),
            ("22in", "22in"),
            ("24in", "24in"),
            ("26in", "26in"),
            ("27.5in", "27.5in"),
            ("29in", "29in"),
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

    def clean(self):
        super().clean()
        if (
            not self.image
            and not self.image_2
            and not self.image_3
            and not self.image_4
        ):
            raise ValidationError("At least one image is required.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for image_field in [self.image, self.image_2, self.image_3, self.image_4]:
            if image_field:
                image_path = image_field.path
                img = Image.open(image_path)
                if img.height > 800 or img.width > 800:
                    output_size = (800, 800)
                    img.thumbnail(output_size)
                    # Save the resized image to a temporary file
                    with tempfile.NamedTemporaryFile(
                        suffix=".jpg", dir=os.path.dirname(image_path), delete=False
                    ) as temp_file:
                        temp_file_name = temp_file.name
                        img.save(temp_file_name)
                        # Replace the original image with the resized one
                        with open(temp_file_name, "rb") as f:
                            with image_field.open("wb") as new_image:
                                new_image.write(f.read())
                    # Delete the temporary file
                    os.remove(temp_file_name)
        # Call the super save method again to save the changes
        super().save(*args, **kwargs)

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
