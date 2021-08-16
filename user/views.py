from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView
from django.views.generic.list import ListView

from user.forms import AddUserToCrewForm, CrewForm, LoginForm, UserForm
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

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        form.save_m2m()
        res = super().form_valid(form)
        instance.user.add(self.request.user)
        return res


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


def add_user_to_crew(request, pk):
    crew = get_object_or_404(Crew, pk=pk)
    if request.method == "POST":
        if request.user in crew.user.all():
            form = AddUserToCrewForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data["user_email"]
                try:
                    user = User.objects.get(email=email)
                    crew.user.add(user)
                    messages.success(
                        request, f"User {user} was added to your crew"
                    )
                    return redirect("user:crew-details", pk=pk)
                except User.DoesNotExist:
                    messages.warning(
                        request,
                        "User with that email does not exists",
                    )

        else:
            HttpResponseForbidden()
    else:
        form = AddUserToCrewForm()
    return render(request, "crew/add-user-to-crew.html", {"form": form})
