from django import forms

from .models import Item


class CustomClearableFileInput(forms.ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        # Remove the "Currently:" text
        html = html.replace("Currently:", "")
        # Remove the "Change:" text
        html = html.replace("Change:", "")
        return html


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
            "image": CustomClearableFileInput(),
            "image_2": CustomClearableFileInput(),
            "image_3": CustomClearableFileInput(),
            "image_4": CustomClearableFileInput(),
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
            "image": CustomClearableFileInput(),
            "image_2": CustomClearableFileInput(),
            "image_3": CustomClearableFileInput(),
            "image_4": CustomClearableFileInput(),
        }
