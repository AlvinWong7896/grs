from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
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


# def signup(request):
#     if request.method == "POST":
#         form = SignupForm(request.POST)

#         if form.is_valid():
#             form.save()
#             return redirect("/login/")  # Redirect only if the form is valid
#     else:
#         form = SignupForm()
#     return render(request, "core/signup.html", {"form": form})


def signupuser(request):
    if request.method == "GET":
        return render(request, "core/signupuser.html", {"form": UserCreationForm()})
    else:
        # Create a new user
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"]
                )
                user.save()
                login(request, user)
                return redirect("home")

            except IntegrityError:
                return render(
                    request,
                    "core/signupuser.html",
                    {
                        "form": UserCreationForm(),
                        "error": "The username has already been taken, please choose a new username",
                    },
                )
        else:
            # Tell the user the passwords didn't match
            return render(
                request,
                "core/signupuser.html",
                {"form": UserCreationForm(), "error": "Passwords did not match"},
            )


def loginuser(request):
    if request.method == "GET":
        return render(request, "core/loginuser.html", {"form": AuthenticationForm()})
    else:
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
            return redirect("core:home")


@login_required
def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect("core:home")
    else:
        return redirect("core:home")
