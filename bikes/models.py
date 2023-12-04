from django.db import models


class Appointment(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact_number = models.SmallIntegerField()
    email_address = models.EmailField()

    def __str__(self):
        return self.first_name + " " + self.last_name


from django.db import models


class Bike(models.Model):
    name = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    new_price = models.DecimalField(max_digits=8, decimal_places=2)
    selling_price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(max_length=800, default="")

    # Add a foreign key to the Photo model
    main_photo = models.ForeignKey(
        "Photo",
        on_delete=models.SET_NULL,
        null=True,
        related_name="main_photo_of",
        blank=True,
    )

    def __str__(self):
        return self.name


class Photo(models.Model):
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="bike_photos/")
    is_main_photo = models.BooleanField(default=False)

    def __str__(self):
        return f"Photo for {self.bike.name}"

    # Optional: You can override the save method to ensure only one main photo per bike
    def save(self, *args, **kwargs):
        if self.is_main_photo:
            # Set all other photos for the same bike as not main
            Photo.objects.filter(bike=self.bike).exclude(pk=self.pk).update(
                is_main_photo=False
            )
        super(Photo, self).save(*args, **kwargs)
