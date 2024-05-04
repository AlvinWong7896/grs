from django import forms

from .models import Item


class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (
            "category",
            "name",
            # "is_sold",
            "material",
            "drivetrain",
            "tire_size",
            "brake_type",
            "description",
            "price",
            "image",
            "image_2",
            "image_3",
            "image_4",
        )
        widgets = {
            "description": forms.Textarea(),
        }


class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (
            "category",
            "name",
            "is_sold",
            "material",
            "drivetrain",
            "tire_size",
            "brake_type",
            "description",
            "price",
            "image",
            "image_2",
            "image_3",
            "image_4",
        )
        widgets = {
            "description": forms.Textarea(),
        }
