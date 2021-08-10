from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from user.models import Crew

from .utils import get_random_code

STATUS_CHOICES = [
    ("complete", "Complete"),
    ("in_progress", "In progress"),
    ("not_started", "Not started"),
    ("on_hold", "On hold"),
]
PRIORITY_CHOICES = (
    ("1", "Low"),
    ("2", "Medium"),
    ("3", "High"),
)


class Task(models.Model):
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="tasks"
    )
    task_name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(
        max_length=11, choices=STATUS_CHOICES, default="not_started"
    )
    priority = models.CharField(
        max_length=15, choices=PRIORITY_CHOICES, default="1"
    )
    assigned_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="user_tasks"
    )
    due_date = models.DateField()

    class Meta:
        ordering = ("-priority", "-due_date")

    def get_absolute_url(self):
        return reverse("task:details")

    def __str__(self):
        return self.task_name


class Project(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True, max_length=80)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
    )
    crew = models.ForeignKey(
        Crew, on_delete=models.CASCADE, related_name="projects"
    )
    dead_line = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("project:details", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        if self.slug:
            return
        if self.name:
            to_slug = slugify(str(self.name))
            if to_slug == "":
                to_slug = str(self.name)
            ex = Project.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug + " " + str(get_random_code()))
                ex = Project.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.name)
        self.slug = to_slug
        super().save(*args, **kwargs)
