from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView
from django.views.generic.list import ListView

from user.forms import CrewForm, LoginForm, UserForm
from user.models import Crew, User


class CreateUserView(CreateView):
    """Create a new user"""

    model = User
    form_class = UserForm
    template_name = "user/create.html"


class CreateCrewView(LoginRequiredMixin, CreateView):
    """Create a new crew"""

    model = Crew
    form_class = CrewForm
    template_name = "crew/create.html"


class CrewDetailView(LoginRequiredMixin, DetailView):
    """Retrive crew details"""

    model = Crew
    template_name = "crew/details.html"


class CrewListView(LoginRequiredMixin, ListView):
    """Retrivie crews"""

    model = Crew
    template_name = "crew/list.html"

    def get_queryset(self):
        return Crew.objects.filter(user=self.request.user)


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = "user/login.html"


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect("user:user-login")
