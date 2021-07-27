from django.views.generic import CreateView

from user.forms import UserForm
from user.models import User


class CreateUserView(CreateView):
    model = User
    form_class = UserForm
    template_name = "create.html"
