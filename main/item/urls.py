from django.urls import path
from . import views

app_name = "item"

urlpatterns = [
    path("", views.marketplace, name="marketplace"),
    path("category/<int:category_id>/", views.marketplace, name="category_marketplace"),
    path("search/", views.search, name="search"),
    path("new/", views.new, name="new"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/edit/", views.edit, name="edit"),
]
