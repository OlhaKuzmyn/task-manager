from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from manager.models import Task, TaskType, Project, Team, Worker, Position


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
        widget=forms.CheckboxInput()
    )


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        required=False,
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "deadline": forms.DateInput(attrs={
                "type": "date",
            })
        }


class WorkerCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "email", "position", "team"
        )


class WorkerUpdateForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("password", None)

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = (
            "username", "first_name", "last_name", "email", "position", "team",
        )


class TeamUpdateForm(forms.ModelForm):
    workers = forms.ModelMultipleChoiceField(
        required=False,
        queryset=get_user_model().objects.filter(team=None),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Team
        fields = ("name", "projects" , "workers",)


class WorkerSearchForm(forms.Form):
    last_name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Search by last name",
        })
    )
    position = forms.ModelChoiceField(
        required=False,
        queryset=Position.objects.all(),
        label="",
        empty_label="All positions",
    )
    team = forms.ModelChoiceField(
        required=False,
        queryset=Team.objects.all(),
        label="",
        empty_label="All teams",
    )


class PositionSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Search by name",
        })
    )