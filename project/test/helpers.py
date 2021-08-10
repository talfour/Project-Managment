from project.models import Project, Task
from user.models import Crew, User


def create_default_user():
    return User.objects.create_user(
        email="test@gmail.com", password="testpass123"
    )


def create_default_crew():
    return Crew.objects.create(name="test")


def create_default_project():
    return Project.objects.create(
        name="test",
        description="test_desc",
        owner=create_default_user(),
        crew=create_default_crew(),
        dead_line="2021-12-20",
    )


def create_default_task(project):
    return Task.objects.create(
        project=project,
        task_name="test_task",
        description="test_desc",
        due_date="2021-12-21",
    )
