from django import forms

from .models import Project, Task


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
        )
        widgets = {"due_date": DateInput()}


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "crew", "dead_line"]
        widgets = {"dead_line": DateInput()}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(ProjectCreateForm, self).__init__(*args, **kwargs)
        self.fields["crew"].queryset = user.crew.all()
