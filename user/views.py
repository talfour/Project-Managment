from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView
from django.views.generic.list import ListView
from project.models import Project
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import views as auth_views
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


@login_required
def user_details(request):
    user = User.objects.get(id=request.user.id)
    user_projects = Project.objects.filter(crew__in=user.crew.all())
    return render(
        request,
        "user/details.html",
        {"user": user, "user_projects": user_projects},
    )


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'user/login.html'


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect("user:user-login")
