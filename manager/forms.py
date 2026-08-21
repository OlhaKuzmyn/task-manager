from black.brackets import Priority
from django import forms
from django.contrib.auth import get_user_model

from manager.models import Task, TaskType, Project


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Search by name",
        })
    )
    deadline = forms.DateField(
        required=False,
        label="Deadline on before",
        widget=forms.DateInput(
            attrs={
            "placeholder": "Search by deadline",
            "type": "date",
        }
        )
    )
    is_completed = forms.BooleanField(
        initial=False,
        required=False,
        label="Completed",
        widget=forms.CheckboxInput()
    )
    priority = forms.ChoiceField(
        required=False,
        label="",
        choices=[("", "All priorities")] + Task.Priority.choices,
    )
    task_type = forms.ModelChoiceField(
        required=False,
        queryset=TaskType.objects.all(),
        empty_label="All task types",
    )
    project = forms.ModelChoiceField(
        required=False,
        queryset=Project.objects.all(),
        empty_label="All projects",
    )
    no_assignees = forms.BooleanField(
        initial=False,
        required=False,
        label="No assignees",
        widget=forms.CheckboxInput()
    )
