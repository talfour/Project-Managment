from django.test import TestCase
from project.forms import (
    DUPLICATE_ITEM_ERROR,
    EMPTY_ITEM_ERROR,
    ProjectCreateForm,
    TaskForm,
)
from project.models import Project, Task
from user.models import Crew, User

from project.test.helpers import create_default_project, create_default_user


class ProjectFormTest(TestCase):
    def test_form_item_input_has_placeholder(self):
        user = create_default_user()
        form = ProjectCreateForm(user=user)
        self.assertIn('placeholder="Enter project title"', form.as_p())

    def test_form_validation_for_blank_items(self):
        user = create_default_user()
        form = ProjectCreateForm(user=user, data={"name": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["name"], [EMPTY_ITEM_ERROR])


class TaskFormTest(TestCase):
    def test_form_renders_item_text_input(self):
        project = create_default_project()
        form = TaskForm(slug=project.slug)
        self.assertIn('placeholder="Enter task title', form.as_p())

    def test_form_validation_for_duplicate_items(self):
        user = User.objects.create_user(
            email="test@gmail.com", password="test1234pass"
        )
        crew = Crew.objects.create(name="test")
        crew.user.add(user)
        project = Project.objects.create(
            name="test",
            slug="test",
            description="test_desc",
            owner=user,
            crew=crew,
            dead_line="2021-12-20",
        )
        Task.objects.create(
            project=project,
            task_name="test",
            description="desc",
            due_date="2021-07-21",
        )
        form = TaskForm(
            slug=project.slug,
            data={
                "project": project,
                "task_name": "test",
                "description": "desc",
                "due_date": "2021-07-21",
                "status": "complete",
                "priority": "1",
            },
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["__all__"], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        user = User.objects.create_user(
            email="test@gmail.com", password="test1234pass"
        )
        crew = Crew.objects.create(name="test")
        crew.user.add(user)
        project = Project.objects.create(
            name="test",
            slug="test",
            description="test_desc",
            owner=user,
            crew=crew,
            dead_line="2021-12-20",
        )
        form = TaskForm(
            slug=project.slug,
            data={
                "project": project,
                "task_name": "test",
                "description": "desc",
                "due_date": "2021-07-21",
                "priority": "1",
                "status": "complete",
            },
        )
        new_item = form.save()
        self.assertEqual(new_item, Task.objects.all()[0])
