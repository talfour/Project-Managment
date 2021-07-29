from django.urls import path

from project import views

app_name = "project"

urlpatterns = [
    path("", views.ProjectListView.as_view(), name="projects"),
    path(
        "project/create/",
        views.ProjectCreateView.as_view(),
        name="project_create",
    ),
    path(
        "project/<slug:slug>",
        views.ProjectDetailView.as_view(),
        name="details",
    ),
    path(
        "project/<slug:slug>/create-task/",
        views.task_create,
        name="create_task",
    ),
]
