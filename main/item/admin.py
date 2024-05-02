from django import forms
from django.contrib import admin
from .models import Category, Item


class CustomSelect(forms.Select):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.option_prefix = ""

    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        option = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )
        if "option_prefix" in self.__dict__:
            option["label"] = option["label"].replace(self.option_prefix, "", 1)
        return option


class ItemAdminForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"


class ItemAdmin(admin.ModelAdmin):
    form = ItemAdminForm
    list_display = (
        "name",
        "category",
        "price",
        "is_sold",
    )  # Add other fields you want to display in the list view
    search_fields = ["name", "category__name"]  # Add fields for search functionality
    list_filter = ("category", "is_sold")  # Add fields for filtering


admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
# admin.site.register(Item)
