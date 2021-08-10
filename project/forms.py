from django import forms
from django.core.exceptions import ValidationError

from .models import Project, Task

EMPTY_ITEM_ERROR = "You can't have an empty title"
DUPLICATE_ITEM_ERROR = "Task with this title alread exists in your project"


class DateInput(forms.DateInput):
    input_type = "date"


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            "task_name",
            "description",
            "status",
            "priority",
            "due_date",
            "project",
        )
        widgets = {
            "due_date": DateInput(),
            "task_name": forms.fields.TextInput(
                attrs={"placeholder": "Enter task title"}
            ),
            "project": forms.HiddenInput(),
        }
        error_messages = {"task_name": {"required": EMPTY_ITEM_ERROR}}

    def clean(self):
        task_name = self.cleaned_data["task_name"]
        project = self.cleaned_data["project"]
        matching_tasks = Task.objects.filter(task_name=task_name).filter(
            project=project
        )
        if self.instance:
            matching_tasks = matching_tasks.exclude(pk=self.instance.pk)
        if matching_tasks.exists():
            msg = DUPLICATE_ITEM_ERROR
            raise ValidationError(msg)
        else:
            return self.cleaned_data

    def __init__(self, *args, **kwargs):
        project = kwargs.pop("slug")
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields["project"].initial = Project.objects.get(slug=project)


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "crew", "dead_line"]
        widgets = {
            "dead_line": DateInput(),
            "name": forms.fields.TextInput(
                attrs={"placeholder": "Enter project title"}
            ),
        }
        error_messages = {"name": {"required": EMPTY_ITEM_ERROR}}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(ProjectCreateForm, self).__init__(*args, **kwargs)
        self.fields["crew"].queryset = user.crew.all()
