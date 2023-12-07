# bikes (app)/views.py

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import BookingForm, BikeForm, CustomUserCreationForm, BikePhotoForm
from .models import Bike, Photo


def home(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def book(request):
    form = BookingForm()
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {"form": form}
    return render(request, "book.html", context)


def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            return redirect("home")  # Redirect to the desired page after registration
        else:
            form = CustomUserCreationForm()

        return render(request, "registration/register.html", {"form": form})


def is_manager(user):
    return user.groups.filter(name="Manager").exists()


manager_required = user_passes_test(is_manager)


def menu(request):
    bikes = Bike.objects.all()
    is_manager_flag = request.user.is_authenticated and is_manager(request.user)
    context = {"bikes": bikes, "is_manager": is_manager_flag}
    # context = {"bikes": bikes, "user": request.user}
    return render(request, "menu.html", context)


@login_required
@manager_required
def create_bike(request):
    if request.method == "POST":
        bike_form = BikeForm(request.POST)
        bike_photo_form = BikePhotoForm(request.POST, request.FILES)

        if bike_form.is_valid() and bike_photo_form.is_valid():
            # Save the bike record
            bike = bike_form.save()

            # Save the bike photo
            bike_photo = bike_photo_form.save(commit=False)
            bike_photo.bike = bike
            bike_photo.save()

            return redirect("menu")

    else:
        bike_form = BikeForm()
        bike_photo_form = BikePhotoForm()

    return render(
        request,
        "create_bike.html",
        {"bike_form": bike_form, "bike_photo_form": bike_photo_form},
    )


@login_required
def update_bike(request, bike_id):
    if not request.user.is_manager:
        # Redirect or show a message for non-manager users
        return redirect("menu")

    bike = get_object_or_404(Bike, id=bike_id)
    if request.method == "POST":
        bike_form = BikeForm(request.POST, instance=bike)
        photo_form = PhotoForm(request.POST, request.FILES, instance=bike.main_photo)

        if bike_form.is_valid() and photo_form.is_valid():
            bike = bike_form.save()
            photo = photo_form.save(commit=False)
            photo.bike = bike
            photo.save()

            return redirect("menu")

    else:
        bike_form = BikeForm(instance=bike)
        photo_form = PhotoForm(instance=bike.main_photo)

    return render(
        request, "update_bike.html", {"bike_form": bike_form, "photo_form": photo_form}
    )


@login_required
def delete_bike(request, bike_id):
    if not request.user.is_manager:
        # Redirect or show a message for non-manager users
        return redirect("menu")

    bike = get_object_or_404(Bike, id=bike_id)
    bike.delete()
    return redirect("menu")


def display_menu_item(request, pk):
    bike = get_object_or_404(Bike, pk=pk)
    context = {"bike": bike}
    return render(request, "display_menu_item.html", context)


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            return redirect("home")  # Redirect to the desired page after registration
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/register.html", {"form": form})


def verify_otp(request):
    if request.method == "POST":
        otp_entered = request.POST.get("otp")
        user = request.user

        # Check if OTP is correct and not expired
        if (
            user.otp == otp_entered
            and (timezone.now() - user.otp_created_at).seconds < 30
        ):
            user.is_verified = True
            user.save()
            return HttpResponse("OTP verified successfully!")
        else:
            return HttpResponse("Invalid OTP or expired. Please request a new OTP.")

    return render(request, "verify_otp.html")
