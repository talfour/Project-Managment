from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils.html import escape
from project.forms import EMPTY_ITEM_ERROR, TaskForm
from project.models import Project, Task
from project.test.helpers import (
    create_default_crew,
    create_default_project,
    create_default_task,
)
from user.models import User


class HomePageTestUserLoggedIn(TestCase):
    def setUp(self):
        self.client.force_login(
            User.objects.get_or_create(email="testmail@gmail.com")[0]
        )
        self.user = User.objects.get(email="testmail@gmail.com")

    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


class NewProjectTest(TestCase):
    def setUp(self):
        self.client.force_login(
            User.objects.get_or_create(email="testmail@gmail.com")[0]
        )
        self.user = User.objects.get(email="testmail@gmail.com")
        self.crew = create_default_crew()
        self.crew.user.add(self.user)

    def test_can_save_a_POST_request(self):
        self.client.post(
            reverse("project:project_create"),
            data={
                "name": "test_pro",
                "description": "desc",
                "crew": self.crew.id,
                "dead_line": "2022-08-22",
            },
        )
        self.assertEqual(Project.objects.count(), 1)
        new_project = Project.objects.first()
        self.assertEqual(new_project.name, "test_pro")

    def test_redirects_after_POST(self):
        response = self.client.post(
            reverse("project:project_create"),
            data={
                "name": "test_pro",
                "description": "desc",
                "crew": self.crew.id,
                "dead_line": "2022-08-22",
            },
        )
        new_project = Project.objects.first()
        self.assertRedirects(
            response,
            reverse("project:details", kwargs={"slug": new_project.slug}),
        )

    def test_form_invalid_input_renders_create_project_template(self):
        response = self.client.post(
            reverse("project:project_create"), data={"name": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project/create.html")

    def test_validation_errors_are_shown_on_project_template(self):
        response = self.client.post(
            reverse("project:project_create"), data={"name": ""}
        )
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_invalid_project_arent_saved(self):
        self.client.post(
            reverse("project:project_create"),
            data={
                "name": "",
                "description": "desc",
                "crew": self.crew.id,
                "dead_line": "2022-08-22",
            },
        )
        self.assertEqual(Project.objects.count(), 0)

    def test_project_update(self):
        self.client.post(
            reverse("project:project_create"),
            data={
                "name": "testpro",
                "description": "desc",
                "crew": self.crew.id,
                "dead_line": "2022-08-22",
            },
        )
        response = self.client.post(
            reverse("project:update", kwargs={"slug": "testpro"}),
            data={"description": "another test"},
        )
        print(response)
        self.assertContains(response, "another test")

    def test_project_delete(self):
        project = Project.objects.create(
            name="test",
            slug="test",
            description="test_desc",
            owner=self.user,
            crew=self.crew,
            dead_line="2021-12-20",
        )

        self.client.post(
            reverse("project:delete_project", kwargs={"slug": project.slug})
        )

        self.assertEqual(0, Project.objects.count())


class TaskViewTest(TestCase):
    def setUp(self):
        self.client.force_login(
            User.objects.get_or_create(email="testmail@gmail.com")[0]
        )
        self.factory = RequestFactory()
        self.user = User.objects.get(email="testmail@gmail.com")
        self.crew = create_default_crew()
        self.crew.user.add(self.user)

    def test_create_task(self):
        project = Project.objects.create(
            name="test",
            description="test_desc",
            owner=self.user,
            crew=self.crew,
            dead_line="2021-12-20",
        )
        task = create_default_task(project)
        response = self.client.get(
            reverse(
                "project:task_details",
                kwargs={"slug": project.slug, "id": task.id},
            )
        )
        self.assertTemplateUsed(response, "task/details.html")

    def test_displays_task_form(self):
        project = create_default_project()
        response = self.client.get(
            reverse("project:task_create", kwargs={"slug": project.slug})
        )
        self.assertIsInstance(response.context["form"], TaskForm)
        self.assertContains(response, 'name="task_name"')

    def test_displays_only_tasks_for_that_project(self):
        project = Project.objects.create(
            name="test",
            description="test_desc",
            owner=self.user,
            crew=self.crew,
            dead_line="2021-12-20",
        )
        Task.objects.create(
            project=project,
            task_name="Task1",
            description="testdesc",
            due_date="2021-12-12",
        )
        Task.objects.create(
            project=project,
            task_name="Task2",
            description="testdesc",
            due_date="2021-12-12",
        )
        other_project = Project.objects.create(
            name="test1",
            description="test_desc",
            owner=self.user,
            crew=self.crew,
            dead_line="2021-12-21",
        )
        Task.objects.create(
            project=other_project,
            task_name="Other_task",
            description="testdesc",
            due_date="2021-12-12",
        )
        Task.objects.create(
            project=other_project,
            task_name="Other_task2",
            description="testdesc",
            due_date="2021-12-12",
        )

        response = self.client.get(
            reverse("project:details", kwargs={"slug": project.slug})
        )
        self.assertContains(response, "Task1")
        self.assertContains(response, "Task2")
        self.assertNotContains(response, "Other_task")
        self.assertNotContains(response, "Other_task2")

    def test_display_task_update(self):
        project = Project.objects.create(
            name="test",
            description="test_desc",
            owner=self.user,
            crew=self.crew,
            dead_line="2021-12-20",
        )
        task = create_default_task(project)

        response = self.client.get(
            reverse(
                "project:task_update",
                kwargs={"slug": project.slug, "id": task.id},
            )
        )
        self.assertContains(response, task.task_name)
        self.assertContains(response, "Update")
