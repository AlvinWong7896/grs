from django.shortcuts import render
from .forms import BookingForm
from .models import Bike


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


def menu(request):
    # Retrieve all Bike objects
    bikes = Bike.objects.all()

    # Prepare a list to store each bike's data along with its main photo
    bikes_with_photos = []

    for bike in bikes:
        # Get the main photo for each bike
        main_photo = bike.main_photo.image.url if bike.main_photo else None

        # Collect other relevant data for each bike
        bike_data = {
            "id": bike.id,
            "name": bike.name,
            "model": bike.model,
            "new_price": bike.new_price,
            "selling_price": bike.selling_price,
            "description": bike.description,
            "main_photo": main_photo,
            # Additional fields or methods can be added as needed
        }

        # Append the bike data to the list
        bikes_with_photos.append(bike_data)

    # Pass the list of bikes with photos to the template
    context = {"menu": bikes_with_photos}
    return render(request, "menu.html", context)


from django.shortcuts import render, redirect
from .models import Bike, Photo
from .forms import BikeForm, PhotoForm


def create_bike(request):
    if request.method == "POST":
        bike_form = BikeForm(request.POST)
        photo_form = PhotoForm(request.POST, request.FILES)

        if bike_form.is_valid() and photo_form.is_valid():
            bike = bike_form.save()
            photo = photo_form.save(commit=False)
            photo.bike = bike
            photo.is_main_photo = True  # Set the first uploaded photo as the main photo
            photo.save()

            return redirect("menu")

    else:
        bike_form = BikeForm()
        photo_form = PhotoForm()

    return render(
        request, "create_bike.html", {"bike_form": bike_form, "photo_form": photo_form}
    )


from django.shortcuts import render
from .models import Bike


def menu(request):
    bikes = Bike.objects.all()
    context = {"bikes": bikes}
    return render(request, "menu.html", context)


from django.shortcuts import render, get_object_or_404, redirect
from .models import Bike, Photo
from .forms import BikeForm, PhotoForm


def update_bike(request, bike_id):
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


from django.shortcuts import get_object_or_404, redirect
from .models import Bike


def delete_bike(request, bike_id):
    bike = get_object_or_404(Bike, id=bike_id)
    bike.delete()
    return redirect("menu")
