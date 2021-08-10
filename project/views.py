import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse
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
        tasks = Task.objects.filter(project=self.object)
        tasks_on_hold = list(
            filter(lambda task: task.status == "on_hold", tasks)
        )
        tasks_not_started = list(
            filter(lambda task: task.status == "not_started", tasks)
        )
        tasks_in_progress = list(
            filter(lambda task: task.status == "in_progress", tasks)
        )
        tasks_complete = list(
            filter(lambda task: task.status == "complete", tasks)
        )
        context["on_hold"] = tasks_on_hold
        context["not_started"] = tasks_not_started
        context["in_progress"] = tasks_in_progress
        context["complete"] = tasks_complete
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

    def get_success_url(self):
        return reverse("project:details", kwargs={"slug": self.object.slug})


@login_required
def task_create(request, slug):
    """Create a new task related to existing project"""
    project = get_object_or_404(Project, slug=slug)
    if request.method == "POST":
        form = TaskForm(request.POST, slug=slug)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.project = project
            obj.save()
            return redirect(
                "project:details",
                slug=project.slug,
            )
    else:
        form = TaskForm(slug=slug)
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


@login_required
def task_status_change(request):
    try:
        new_status = json.loads(request.body.decode("UTF-8"))["new_status"]
    except KeyError:
        return JsonResponse({"message": "There was an error with new status"})
    if new_status not in ("complete", "in_progress", "not_started", "on_hold"):
        return JsonResponse(
            {"message": "There was an error with new status"}, status=400
        )
    task_id = json.loads(request.body.decode("UTF-8"))["task_id"]
    project = Project.objects.get(tasks__in=task_id)
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        if request.user not in project.crew.user.all():
            return HttpResponseForbidden()
        task.status = new_status
        task.save()
        return JsonResponse(
            {"message": "Task status changed", "task": task.status}, status=200
        )


@login_required
def task_assign_user(request):
    try:
        task_id = json.loads(request.body.decode("UTF-8"))["task_id"]
    except ValueError:
        return JsonResponse(
            {"message": "There was an error while reading task_id"}, status=400
        )
    except KeyError:
        return JsonResponse(
            {"message": "There was an error while reading task_id"}, status=400
        )
    project = Project.objects.get(tasks__in=task_id)
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        if request.user not in project.crew.user.all():
            return HttpResponseForbidden()
        if task.status == "complete":
            return HttpResponseForbidden(
                "You cannot assign yourself to task which is completed"
            )
        task.assigned_by.add(request.user)
        return JsonResponse(
            {"message": "You were assigned to this task"}, status=200
        )


@login_required
def home_page(request):
    user = request.user
    user_tasks = Task.objects.filter(assigned_by=request.user)
    active_tasks = user_tasks.exclude(status="complete")
    total_tasks_completed = user_tasks.filter(status="complete")
    projects = Project.objects.filter(crew__in=user.crew.all())

    return render(
        request,
        "home.html",
        {
            "user_tasks": user_tasks,
            "active_tasks": active_tasks,
            "tasks_completed": total_tasks_completed,
            "projects": projects,
        },
    )


@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, id=id)
    if request.user != task.project.owner:
        return HttpResponseForbidden(
            "You must be project owner to delete task"
        )
    task.delete()
    return redirect("project:details", slug=task.project.slug)
