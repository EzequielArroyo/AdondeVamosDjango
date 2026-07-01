from django.urls import path

from .views import (
    RegisterView,
    ProfileDetailView,
    ProfileUpdateView
)
app_name = "users"
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileDetailView.as_view(), name="profile"),
    path("profile/update/", ProfileUpdateView.as_view(), name="profile_update",
    ),
]