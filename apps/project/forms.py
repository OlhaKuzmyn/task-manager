from django import forms


class ProjectSearchForm(forms.Form):
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
    no_tasks = forms.BooleanField(
        initial=False,
        required=False,
        label="No tasks",
        widget=forms.CheckboxInput()
    )
