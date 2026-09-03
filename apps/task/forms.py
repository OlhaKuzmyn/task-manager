from django import forms
from django.contrib.auth import get_user_model

from apps.project.models import Project
from apps.task.models import Task
from apps.task_type.models import TaskType


class TaskSearchForm(forms.Form):
    FILTER_CHOICES = [
        ("mine", "My tasks"),
        ("mine_and_team", "My and team tasks"),
        ("team", "Team tasks"),
        ("all", "All tasks"),
    ]
    filter_select = forms.ChoiceField(
        choices=FILTER_CHOICES,
        required=False,
        label="Filter",
        widget=forms.RadioSelect,
    )
    assigned_to_me = forms.BooleanField(
        required=False,
        initial=True,
        label="Assigned to me",
        widget=forms.CheckboxInput(),
    )
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name",
            }
        ),
    )
    deadline = forms.DateField(
        required=False,
        label="Deadline on before",
        widget=forms.DateInput(
            attrs={
                "placeholder": "Search by deadline",
                "type": "date",
            }
        ),
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
        label="",
        empty_label="All task types",
    )
    project = forms.ModelChoiceField(
        required=False,
        queryset=Project.objects.all(),
        label="",
        empty_label="All projects",
    )
    no_assignees = forms.BooleanField(
        initial=False,
        required=False,
        label="No assignees",
        widget=forms.CheckboxInput(),
    )


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        required=False,
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "deadline": forms.DateInput(
                attrs={
                    "type": "date",
                }
            )
        }
