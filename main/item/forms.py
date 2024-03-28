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
            "frame_size",
            "tire_size",
            "brake_type",
            "description",
            "price",
            "image",
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
            "frame_size",
            "tire_size",
            "brake_type",
            "description",
            "price",
            "image",
        )
        widgets = {
            "description": forms.Textarea(),
        }
