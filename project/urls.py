from django.urls import path

from project import views

app_name = "project"

urlpatterns = [
    path("", views.ProjectListView.as_view(), name="projects"),
    path(
        "project/task-status-change/",
        views.task_status_change,
        name="task_change",
    ),
    path(
        "project/create/",
        views.ProjectCreateView.as_view(),
        name="project_create",
    ),
    path(
        "project/<slug:slug>/",
        views.ProjectDetailView.as_view(),
        name="details",
    ),
    path(
        "project/<slug:slug>/create-task/",
        views.task_create,
        name="task_create",
    ),
    path(
        "project/<slug:slug>/task/<int:id>/",
        views.task_details,
        name="task_details",
    ),
]
