
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add/", views.add_project, name="add_project"),
    path(
        "detail/<int:project_id>/",
        views.project_detail,
        name="project_detail"
    ),
    path(
        "edit/<int:project_id>/",
        views.edit_project,
        name="edit_project"
    ),
    path("delete/<int:project_id>/",
         views.delete_project, name="delete_project"),
]
