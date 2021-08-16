from django import template
from user.models import User

register = template.Library()


@register.simple_tag
def get_tasks_done_in_specific_crew(user_email, projects):
    user = User.objects.get(email=user_email)
    user_tasks_completed = (
        user.user_tasks.all()
        .filter(status="complete")
        .filter(project__in=projects)
        .count()
    )
    return user_tasks_completed


@register.simple_tag
def get_assigned_tasks_in_specific_crew(user_email, projects):
    user = User.objects.get(email=user_email)
    assigned_tasks = (
        user.user_tasks.all()
        .filter(assigned_by=user)
        .filter(project__in=projects)
        .count()
    )
    return assigned_tasks
