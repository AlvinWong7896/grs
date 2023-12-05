from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import secrets


class Appointment(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact_number = models.SmallIntegerField()
    email_address = models.EmailField()

    def __str__(self):
        return self.first_name + " " + self.last_name


class Bike(models.Model):
    name = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    new_price = models.DecimalField(max_digits=8, decimal_places=2)
    selling_price = models.DecimalField(max_digits=7, decimal_places=2)
    location = models.CharField(max_length=50, default="Bishan")
    description = models.TextField(blank=True, null=True)

    STATUS_CHOICES = [
        ("Available", "Available"),
        ("Reserved", "Reserved"),
        ("Sold", "Sold"),
    ]
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Available"
    )

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
    image = models.ImageField(upload_to="photos/")
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


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    # Add related_name to avoid clashes with auth.User model
    groups = models.ManyToManyField(Group, related_name="custom_user_set", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_user_set", blank=True
    )


# Generate OTP and send an email on user registration
@receiver(post_save, sender=CustomUser)
def generate_otp(sender, instance, created, **kwargs):
    if created:
        instance.otp = secrets.token_hex(3).upper()  # Generating a 6-digit OTP
        instance.otp_created_at = timezone.now()
        instance.save()
        send_mail(
            "OTP for Registration",
            f"Your OTP is: {instance.otp}",
            "from@example.com",
            [instance.email],
            fail_silently=False,
        )
