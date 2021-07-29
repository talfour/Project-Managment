from django.views.generic import CreateView

from user.forms import CrewForm, UserForm
from user.models import Crew, User


class CreateUserView(CreateView):
    model = User
    form_class = UserForm
    template_name = "create.html"


class CreateCrewView(CreateView):
    model = Crew
    form_class = CrewForm
    template_name = "crew/create.html"
