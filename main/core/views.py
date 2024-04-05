from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.urls import reverse
from django.utils import timezone
from item.models import Category, Item
from .forms import SignupForm


def home(request):
    return render(request, "core/index.html")


def index(request):
    items = Item.objects.filter(is_sold=False)[0:4]
    categories = Category.objects.all()

    return render(
        request,
        "core/index.html",
        {
            "categories": categories,
            "items": items,
        },
    )


def contact(request):
    return render(request, "core/contact.html")


def signupuser(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("core:home")  # Redirect only if the form is valid
    else:
        form = SignupForm()
    return render(request, "core/signupuser.html", {"form": form})


def loginuser(request):
    if request.method == "GET":
        # Retrieve the 'next' parameter from the query string
        next_url = request.GET.get("next", "")
        print("Next_URL: ", next_url)  # Print the content of 'next' parameter
        return render(request, "core/loginuser.html", {"form": AuthenticationForm()})
    elif request.method == "POST":
        # Ensure CSRF token is correct
        if not request.POST.get("csrfmiddlewaretoken"):
            return render(
                request, "core/loginuser.html", {"error": "CSRF token missing"}
            )

        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "core/loginuser.html",
                {
                    "form": AuthenticationForm(),
                    "error": "Username and password did not match",
                },
            )
        else:
            login(request, user)
            # Redirect to 'next' if it exists, otherwise redirect to core:home
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)
            else:
                return redirect(reverse("core:home"))


@login_required
def logoutuser(request):
    if request.method in ("POST", "GET"):
        logout(request)
        return redirect("core:home")
    else:
        return redirect("core:home")
