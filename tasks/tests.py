from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
import datetime
from .models import Task


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

    def test_task_creation(self):
        task = Task.objects.create(
            user=self.user,
            title="Test Task",
            description="Test Description",
            priority="high",
            category="work",
            due_date=datetime.date.today(),
        )
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.priority, "high")
        self.assertEqual(task.category, "work")
        self.assertFalse(task.completed)
        self.assertEqual(str(task), "Test Task")

    def test_is_overdue(self):
        # Create a task due yesterday (should be overdue)
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        task_overdue = Task.objects.create(
            user=self.user, title="Overdue Task", due_date=yesterday, completed=False
        )
        self.assertTrue(task_overdue.is_overdue)

        # Create a completed task due yesterday (should NOT be overdue because it is completed)
        task_completed_yesterday = Task.objects.create(
            user=self.user,
            title="Completed Yesterday",
            due_date=yesterday,
            completed=True,
        )
        self.assertFalse(task_completed_yesterday.is_overdue)

        # Create a task due tomorrow (should NOT be overdue)
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        task_future = Task.objects.create(
            user=self.user, title="Future Task", due_date=tomorrow, completed=False
        )
        self.assertFalse(task_future.is_overdue)


class TaskViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.task = Task.objects.create(
            user=self.user,
            title="Existing Task",
            priority="medium",
            category="personal",
        )

    def test_anonymous_redirect(self):
        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_task_list_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Existing Task")

    def test_task_create_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(
            reverse("task_create"),
            {
                "title": "New Detailed Task",
                "description": "Created via view",
                "priority": "low",
                "category": "shopping",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirects to task_list
        self.assertTrue(Task.objects.filter(title="New Detailed Task").exists())

    def test_task_edit_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(
            reverse("task_edit", args=[self.task.id]),
            {"title": "Updated Task Name", "priority": "high", "category": "health"},
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task Name")
        self.assertEqual(self.task.priority, "high")

    def test_task_delete_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse("task_delete", args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_task_toggle_ajax(self):
        self.client.login(username="testuser", password="password123")
        self.assertFalse(self.task.completed)

        # Call toggle via post
        response = self.client.post(
            reverse("task_toggle", args=[self.task.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)

        # Verify response JSON
        data = response.json()
        self.assertTrue(data["success"])
        self.assertTrue(data["completed"])

        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)


class AuthViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_view(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "secpass123",
                "password2": "secpass123",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirects to task_list
        self.assertTrue(User.objects.filter(username="newuser").exists())
