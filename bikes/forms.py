from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Appointment, Bike, Photo


# Code added for loading form data on the Booking page
class BookingForm(ModelForm):
    class Meta:
        model = Appointment
        fields = "__all__"


class BikeForm(forms.ModelForm):
    class Meta:
        model = Bike
        fields = [
            "name",
            "model",
            "new_price",
            "selling_price",
            "location",
            "description",
            "status",
        ]


class BikePhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["image", "is_main_photo"]


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "email"]
