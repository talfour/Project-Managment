from django import forms
from django.contrib.auth.forms import UserCreationForm

from user.models import Crew, User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "name"]


class CrewForm(forms.ModelForm):
    class Meta:
        model = Crew
        fields = ("name",)
