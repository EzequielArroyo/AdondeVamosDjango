from django.urls import path

from .views import (
    RegisterView,
    MyProfileView,
    ProfileDetailView,
    ProfileUpdateView,
)
app_name = "users"
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", MyProfileView.as_view(), name="my_profile"),
    path("profile/update/", ProfileUpdateView.as_view(), name="profile_update"),
    path("profile/<int:user_id>/", ProfileDetailView.as_view(), name="profile_detail"),
]