from django.conf import settings
from django.db import models

STATUS_CHOICES = (
    ("done", "Done"),
    ("in_progress", "In progress"),
    ("tracked", "Tracked"),
    ("not_touched", "Not touched"),
)
PRIORITY_CHOICES = (
    ("low", "Low"),
    ("medium", "Medium"),
    ("High", "high"),
)


class Tag(models.Model):
    name = models.CharField(max_length=255)
    task = models.ForeignKey("Task", on_delete=models.CASCADE)


class Section(models.Model):
    name = models.CharField(max_length=255)
    task = models.ForeignKey("Task", on_delete=models.CASCADE)


class Task(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    task_name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default=1)
    priority = models.CharField(
        max_length=15, choices=PRIORITY_CHOICES, default=-1
    )
    assigned_by = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    due_date = models.DateField()
    time_spent = models.DurationField()


class Project(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
    )
    assign = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned",
        blank=True,
    )
    dead_line = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
