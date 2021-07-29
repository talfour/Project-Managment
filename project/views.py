from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, ListView

from .forms import ProjectCreateForm, TaskForm
from .models import Project

# Create your views here.


class ProjectListView(ListView):
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


class ProjectDetailView(DetailView):
    model = Project
    template_name = "project/detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        return context


class ProjectCreateView(CreateView):
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


def task_create(request, slug):
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
