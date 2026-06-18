from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "due_date",
            "priority",
            "category",
            "completed",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "glass-input",
                    "placeholder": "What needs to be done?",
                    "required": True,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "glass-input textarea",
                    "placeholder": "Add a detailed description (optional)...",
                    "rows": 3,
                }
            ),
            "due_date": forms.DateInput(
                attrs={"class": "glass-input date-picker", "type": "date"}
            ),
            "priority": forms.Select(attrs={"class": "glass-input select"}),
            "category": forms.Select(attrs={"class": "glass-input select"}),
            "completed": forms.CheckboxInput(attrs={"class": "glass-checkbox"}),
        }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "glass-input", "placeholder": "Enter your email address"}
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "glass-input", "placeholder": "Choose a username"}
            )
        }
