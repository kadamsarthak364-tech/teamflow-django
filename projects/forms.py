
from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "deadline"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter project name"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter project description",
                "rows": 4
            }),
            "deadline": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
        }
