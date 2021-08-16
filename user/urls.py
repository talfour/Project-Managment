from django.urls import path

from user import views

app_name = "user"

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="user-create"),
    path(
        "crew/create/",
        views.CreateCrewView.as_view(),
        name="crew_create",
    ),
    path(
        "crew/details/<int:pk>/",
        views.CrewDetailView.as_view(),
        name="crew-details",
    ),
    path(
        "crew/details/<int:pk>/add-user/",
        views.add_user_to_crew,
        name="add-user",
    ),
    path("crew/list/", views.CrewListView.as_view(), name="crew-list"),
    path("login/", views.LoginView.as_view(), name="user-login"),
    path("logout/", views.logout_view, name="user-logout"),
]
