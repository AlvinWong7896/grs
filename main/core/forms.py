from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class BaseFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update(
                {
                    "class": "w-full px-6 py-4 rounded-xl",
                }
            )


class LoginForm(AuthenticationForm, BaseFormMixin):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Your username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Your password"})
    )


class SignupForm(UserCreationForm, BaseFormMixin):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Your username"})
    )

    email = forms.CharField(
        widget=forms.EmailInput(attrs={"placeholder": "Your email address"})
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Your password"})
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Repeat password"})
    )
