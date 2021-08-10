from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from user.models import Crew

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
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
