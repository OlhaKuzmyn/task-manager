from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from apps.position.models import Position
from apps.team.models import Team


class WorkerCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "position",
            "team",
        )


class WorkerUpdateForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("password", None)

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "position",
            "team",
        )


class WorkerSearchForm(forms.Form):
    last_name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by last name",
            }
        ),
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
