from django.urls import path

from project import views

app_name = "project"

urlpatterns = [
    path("", views.home_page, name="home"),
    path("projects/", views.ProjectListView.as_view(), name="projects"),
    path("project/delete/<int:id>/", views.delete_task, name="delete"),
    path(
        "project/<slug:slug>/update/",
        views.ProjectUpdateView.as_view(),
        name="update",
    ),
    path(
        "project/<slug:slug>/delete/",
        views.ProjectDeleteView.as_view(),
        name="delete_project",
    ),
    path(
        "project/task-status-change/",
        views.task_status_change,
        name="task_change",
    ),
    path(
        "project/task-assign-user/",
        views.task_assign_user,
        name="task_assign",
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
        "project/<slug:slug>/close-project/",
        views.project_finish,
        name="project_finish",
    ),
    path(
        "project/<slug:slug>/task/<int:id>/",
        views.task_details,
        name="task_details",
    ),
    path(
        "project/<slug:slug>/task/<int:id>/update/",
        views.task_update,
        name="task_update",
    ),
    path("tasks/", views.task_list, name="task_list"),
]
