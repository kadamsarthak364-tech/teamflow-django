
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import Project
from .forms import ProjectForm


@login_required
def home(request):
    projects = Project.objects.filter(
        owner=request.user
    ).order_by("-created_at")

    return render(request, "dashboard/home.html", {
        "projects": projects
    })


@login_required
def add_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect("home")
    else:
        form = ProjectForm()

    return render(request, "projects/add.html", {
        "form": form
    })


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(
        Project,
        id=project_id,
        owner=request.user
    )

    return render(request, "projects/detail.html", {
        "project": project
    })


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(
        Project,
        id=project_id,
        owner=request.user
    )

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ProjectForm(instance=project)

    return render(
        request,
        "projects/edit.html",
        {"form": form, "project": project}
    )


@login_required
@require_POST
def delete_project(request, project_id):
    project = get_object_or_404(
        Project,
        id=project_id,
        owner=request.user
    )

    project.delete()
    return redirect("home")