from django.core.exceptions import ValidationError
from django.test import TestCase
from project.models import Project, Task
from project.test.helpers import (
    create_default_crew,
    create_default_project,
    create_default_user,
)


class TaskModelTest(TestCase):
    def test_default_status_and_priority(self):
        task = Task(
            project=create_default_project(),
            task_name="test",
            description="desc",
            due_date="2021-12-12",
        )
        self.assertEqual(task.status, "not_started")
        self.assertEqual(task.priority, "1")

    def test_task_is_related_to_project(self):
        project = create_default_project()
        task = Task(
            project=project,
            task_name="test",
            description="desc",
            due_date="2021-12-12",
        )
        task.save()
        project.tasks.add(task)
        self.assertIn(task, project.tasks.all())

    def test_cannot_save_empty_project_task(self):
        project = create_default_project()
        task = Task(
            project=project,
            task_name="",
            description="desc",
            due_date="2021-12-12",
        )
        with self.assertRaises(ValidationError):
            task.save()
            task.full_clean()

    def test_string_representation(self):
        project = create_default_project()
        task = Task(
            project=project,
            task_name="blabla",
            description="desc",
            due_date="2021-12-12",
        )
        self.assertEqual(str(task), "blabla")


class ProjectModelTest(TestCase):
    def test_get_absolute_url(self):
        project = create_default_project()
        self.assertEqual(
            project.get_absolute_url(), f"/project/{project.slug}/"
        )

    def test_on_save_slug_is_generated_and_not_duplicated(self):
        user = create_default_user()
        crew = create_default_crew()
        project = Project.objects.create(
            name="test",
            description="test_desc",
            owner=user,
            crew=crew,
            dead_line="2021-12-20",
        )
        project2 = Project.objects.create(
            name="test",
            description="test_desc",
            owner=user,
            crew=crew,
            dead_line="2021-12-20",
        )

        self.assertNotEqual(project.slug, project2.slug)
