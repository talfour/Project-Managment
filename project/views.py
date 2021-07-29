from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, ListView

from .forms import ProjectCreateForm, TaskForm
from .models import Project, Task

# Create your views here.


class ProjectListView(LoginRequiredMixin, ListView):
    """Lists all available projects for logged user"""

    model = Project
    template_name = "project/list.html"
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        user = self.request.user
        crew = user.crew.all()
        queryset = Project.objects.filter(crew__in=crew)
        return queryset


class ProjectDetailView(LoginRequiredMixin, DetailView):
    """Retrieve project details"""

    model = Project
    template_name = "project/detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """Creates a new project"""

    model = Project
    form_class = ProjectCreateForm
    template_name = "project/create.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ProjectCreateView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


@login_required
def task_create(request, slug):
    """Create a new task related to existing project"""
    project = get_object_or_404(Project, slug=slug)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.project = project
            obj.save()
            return redirect(
                "project:details",
                slug=project.slug,
            )
    else:
        form = TaskForm()
    return render(request, "task/create.html", {"form": form})


@login_required
def task_details(request, slug, id):
    project = get_object_or_404(Project, slug=slug)
    if request.user not in project.crew.user.all():
        return HttpResponseForbidden()
    task = get_object_or_404(Task, id=id)
    return render(
        request, "task/details.html", {"task": task, "project": project}
    )
