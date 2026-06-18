from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    CATEGORY_CHOICES = [
        ("personal", "Personal"),
        ("work", "Work"),
        ("shopping", "Shopping"),
        ("health", "Health"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default="medium"
    )
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="personal"
    )
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["completed", "due_date", "-created_at"]

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        import datetime

        if self.due_date and not self.completed:
            return self.due_date < datetime.date.today()
        return False
