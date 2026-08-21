from django import forms
from django.contrib.auth import get_user_model


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
    # priority = forms.ChoiceField(
    #
    # )