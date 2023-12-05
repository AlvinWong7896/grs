from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("book/", views.book, name="book"),
    #     # Add the remaining URL path configurations here
    path("menu/", views.menu, name="menu"),
    path("menu_item/<int:pk>/", views.display_menu_item, name="menu_item"),
    path("create/", views.create_bike, name="create_bike"),
    path("update/<int:bike_id>/", views.update_bike, name="update_bike"),
    path("delete/<int:bike_id>/", views.delete_bike, name="delete_bike"),
    path("register/", views.register, name="register"),
    path("verify_otp/", views.verify_otp, name="verify_otp"),
    path("signup/", views.signup_view, name="signup"),
]
