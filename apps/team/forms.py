from django import forms

from apps.project.models import Project
from apps.team.models import Team


class TeamForm(forms.ModelForm):
    projects = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Project.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Team
        fields = (
            "name",
            "description",
            "projects",
        )


class TeamSearchForm(forms.Form):
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
    projects = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Project.objects.all(),
        label="",
        widget=forms.CheckboxSelectMultiple,
    )
    no_projects = forms.BooleanField(
        initial=False,
        required=False,
        label="No projects",
        widget=forms.CheckboxInput()
    )
    no_team_members = forms.BooleanField(
        initial=False,
        required=False,
        label="No workers",
        widget=forms.CheckboxInput()
    )
