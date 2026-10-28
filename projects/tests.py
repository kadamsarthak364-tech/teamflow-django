from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Project


class ProjectRoleTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.owner = user_model.objects.create_user(username="owner")
        self.other_user = user_model.objects.create_user(username="other")
        self.project = Project.objects.create(
            title="Private project",
            owner=self.owner
        )

    def test_dashboard_only_lists_owned_projects_and_hides_admin_links(self):
        Project.objects.create(title="Other project", owner=self.other_user)
        self.client.force_login(self.owner)

        response = self.client.get(reverse("home"))

        self.assertContains(response, "Private project")
        self.assertNotContains(response, "Other project")
        self.assertNotContains(response, reverse("admin:index"))
        self.assertNotContains(response, reverse("admin_tools"))

    def test_project_detail_is_private_to_its_owner(self):
        self.client.force_login(self.other_user)

        response = self.client.get(
            reverse("project_detail", args=[self.project.id])
        )

        self.assertEqual(response.status_code, 404)

    def test_owner_can_open_project_detail(self):
        self.client.force_login(self.owner)

        response = self.client.get(
            reverse("project_detail", args=[self.project.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Private project")

    def test_staff_user_sees_admin_links(self):
        staff_user = get_user_model().objects.create_user(
            username="staff",
            is_staff=True
        )
        self.client.force_login(staff_user)

        response = self.client.get(reverse("home"))

        self.assertContains(response, reverse("admin:index"))
        self.assertContains(response, reverse("admin_tools"))
