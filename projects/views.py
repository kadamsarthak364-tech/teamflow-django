
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Project
from .forms import ProjectForm


def home(request):
    projects = Project.objects.all().order_by("-created_at")

    return render(request, "dashboard/home.html", {
        "projects": projects
    })


def add_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)

            # Temporary owner for development.
            # We will replace this with logged-in users later.
            project.owner = User.objects.first()

            if project.owner is None:
                return render(request, "projects/add.html", {
                    "form": form,
                    "error": "Create a user in Django Admin first."
                })

            project.save()
            return redirect("home")
    else:
        form = ProjectForm()

    return render(request, "projects/add.html", {
        "form": form
    })


def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        project.delete()
        return redirect("home")

    return redirect("home")
