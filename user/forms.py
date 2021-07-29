from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

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
    username = forms.CharField(label='Email / Username')
