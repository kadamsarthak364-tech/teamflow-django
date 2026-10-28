from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminToolsAccessTests(TestCase):
    def test_normal_user_cannot_access_admin_tools(self):
        user = get_user_model().objects.create_user(username="normal-user")
        self.client.force_login(user)

        response = self.client.get(reverse("admin_tools"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response["Location"])

    def test_staff_user_can_access_admin_tools(self):
        user = get_user_model().objects.create_user(
            username="staff-user",
            is_staff=True
        )
        self.client.force_login(user)

        response = self.client.get(reverse("admin_tools"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to the TeamFlow administration tools.")
