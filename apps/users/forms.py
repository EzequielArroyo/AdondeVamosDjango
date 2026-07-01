from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()


class RegisterForm(UserCreationForm):

    class Meta:
        model = User

        fields = (
            "username",
            "email",
        )

class UserForm(forms.ModelForm):

    class Meta:
        model = User

        fields = (
            "first_name",
            "last_name",
            "email",
        )

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = (
            "city",
            "bio",
        )