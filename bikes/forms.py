from django.forms import ModelForm
from .models import Appointment


# Code added for loading form data on the Booking page
class BookingForm(ModelForm):
    class Meta:
        model = Appointment
        fields = "__all__"
