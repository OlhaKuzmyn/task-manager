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
    # deadline = forms.DateTimeField(
    #     required=False,
    #     label="",
    #     widget=forms.DateTimeInput(attrs={
    #         "placeholder": "Search by deadline",
    #     })
    # )
    # is_completed = forms.BooleanField(
    #     required=False,
    #     label="",
    #     widget=forms.CheckboxInput(attrs={
    #         "checked": "Completed",
    #     })
    # )
    # priority = forms.ChoiceField(
    #
    # )