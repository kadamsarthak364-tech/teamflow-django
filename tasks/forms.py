
from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "project",
            "assigned_to",
            "priority",
            "status",
            "due_date",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter task title"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter task description",
                "rows": 3
            }),
            "project": forms.Select(attrs={
                "class": "form-select"
            }),
            "assigned_to": forms.Select(attrs={
                "class": "form-select"
            }),
            "priority": forms.Select(attrs={
                "class": "form-select"
            }),
            "status": forms.Select(attrs={
                "class": "form-select"
            }),
            "due_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
        }
