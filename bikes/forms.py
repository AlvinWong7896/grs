from django.forms import ModelForm
from .models import Appointment


# Code added for loading form data on the Booking page
class BookingForm(ModelForm):
    class Meta:
        model = Appointment
        fields = "__all__"


# forms.py
from django import forms
from .models import Bike, Photo


class BikeForm(forms.ModelForm):
    class Meta:
        model = Bike
        fields = ["name", "model", "new_price", "selling_price", "description"]


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["image", "is_main_photo"]


# bikes/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "email"]
