
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User

from .models import Task
from .forms import TaskForm
from projects.models import Project


def get_user_task_or_404(request, task_id):
    """Allow access only to tasks in the current user's projects."""
    return get_object_or_404(
        Task,
        id=task_id,
        project__owner=request.user
    )


def configure_task_form(form, request, task=None):
    """Limit project choices to projects owned by the current user."""
    form.fields["project"].queryset = Project.objects.filter(
        owner=request.user
    )

    # Without a project-membership model, allow self-assignment only.
    allowed_users = User.objects.filter(pk=request.user.pk)

    # Preserve an existing assignee when editing a task.
    if task and task.assigned_to_id:
        allowed_users = User.objects.filter(
            pk__in=[request.user.pk, task.assigned_to_id]
        )

    form.fields["assigned_to"].queryset = allowed_users


@login_required
def task_list(request):
    tasks = (
        Task.objects
        .filter(project__owner=request.user)
        .select_related("project", "assigned_to")
        .order_by("-created_at")
    )

    return render(request, "tasks/list.html", {"tasks": tasks})


@login_required
def add_task(request):
    form = TaskForm(request.POST or None)
    configure_task_form(form, request)

    if request.method == "POST" and form.is_valid():
        task = form.save(commit=False)

        # Verify ownership again before saving.
        if task.project.owner_id != request.user.id:
            form.add_error(
                "project",
                "Select one of your own projects."
            )
        else:
            task.save()
            return redirect("task_list")

    return render(request, "tasks/add.html", {"form": form})


@login_required
def edit_task(request, task_id):
    task = get_user_task_or_404(request, task_id)

    form = TaskForm(request.POST or None, instance=task)
    configure_task_form(form, request, task)

    if request.method == "POST" and form.is_valid():
        updated_task = form.save(commit=False)

        if updated_task.project.owner_id != request.user.id:
            form.add_error(
                "project",
                "Select one of your own projects."
            )
        else:
            updated_task.save()
            return redirect("task_list")

    return render(
        request,
        "tasks/edit.html",
        {"form": form, "task": task}
    )


@login_required
@require_POST
def delete_task(request, task_id):
    task = get_user_task_or_404(request, task_id)
    task.delete()
    return redirect("task_list")


@login_required
@require_POST
def update_task_status(request, task_id):
    task = get_user_task_or_404(request, task_id)
    new_status = request.POST.get("status")

    valid_statuses = dict(Task.STATUS_CHOICES)

    if new_status in valid_statuses:
        task.status = new_status
        task.save(update_fields=["status"])

    return redirect("task_list")
