from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from user.models import Crew, User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "name"]


class CrewForm(forms.ModelForm):
    class Meta:
        model = Crew
        fields = ("name",)


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Email / Username")


class AddUserToCrewForm(forms.Form):
    user_email = forms.CharField(label="User email", max_length=100)