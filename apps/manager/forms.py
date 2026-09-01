from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# from manager.models import (
#     # Task,
#     # TaskType,
#     # Project,
#     # Team,
#     # Position
# )


# class TaskSearchForm(forms.Form):
#     FILTER_CHOICES = [
#         ("mine", "My tasks"),
#         ("mine_and_team", "My and team tasks"),
#         ("team", "Team tasks"),
#         ("all", "All tasks"),
#     ]
#     filter_select = forms.ChoiceField(
#         choices=FILTER_CHOICES,
#         required=False,
#         label="Filter",
#         widget=forms.RadioSelect,
#     )
#     assigned_to_me = forms.BooleanField(
#         required=False,
#         initial=True,
#         label="Assigned to me",
#         widget=forms.CheckboxInput()
#     )
#     name = forms.CharField(
#         max_length=255,
#         required=False,
#         label="",
#         widget=forms.TextInput(attrs={
#             "placeholder": "Search by name",
#         })
#     )
#     deadline = forms.DateField(
#         required=False,
#         label="Deadline on before",
#         widget=forms.DateInput(
#             attrs={
#                 "placeholder": "Search by deadline",
#                 "type": "date",
#             }
#         )
#     )
#     is_completed = forms.BooleanField(
#         initial=False,
#         required=False,
#         label="Completed",
#         widget=forms.CheckboxInput()
#     )
#     priority = forms.ChoiceField(
#         required=False,
#         label="",
#         choices=[("", "All priorities")] + Task.Priority.choices,
#     )
#     task_type = forms.ModelChoiceField(
#         required=False,
#         queryset=TaskType.objects.all(),
#         label="",
#         empty_label="All task types",
#     )
#     project = forms.ModelChoiceField(
#         required=False,
#         queryset=Project.objects.all(),
#         label="",
#         empty_label="All projects",
#     )
#     no_assignees = forms.BooleanField(
#         initial=False,
#         required=False,
#         label="No assignees",
#         widget=forms.CheckboxInput()
#     )
#
#
# class TaskForm(forms.ModelForm):
#     assignees = forms.ModelMultipleChoiceField(
#         required=False,
#         queryset=get_user_model().objects.all(),
#         widget=forms.CheckboxSelectMultiple
#     )
#
#     class Meta:
#         model = Task
#         fields = "__all__"
#         widgets = {
#             "deadline": forms.DateInput(attrs={
#                 "type": "date",
#             })
#         }


# class WorkerCreationForm(UserCreationForm):
#
#     class Meta(UserCreationForm.Meta):
#         model = get_user_model()
#         fields = UserCreationForm.Meta.fields + (
#             "first_name", "last_name", "email", "position", "team"
#         )
#
#
# class WorkerUpdateForm(UserChangeForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields.pop("password", None)
#
#     class Meta(UserChangeForm.Meta):
#         model = get_user_model()
#         fields = (
#             "username", "first_name", "last_name", "email", "position", "team",
#         )


# class TeamForm(forms.ModelForm):
#     projects = forms.ModelMultipleChoiceField(
#         required=False,
#         queryset=Project.objects.all(),
#         widget=forms.CheckboxSelectMultiple
#     )
#     class Meta:
#         model = Team
#         fields = ("name", "projects", )


# class WorkerSearchForm(forms.Form):
#     last_name = forms.CharField(
#         max_length=255,
#         required=False,
#         label="",
#         widget=forms.TextInput(attrs={
#             "placeholder": "Search by last name",
#         })
#     )
#     position = forms.ModelChoiceField(
#         required=False,
#         queryset=Position.objects.all(),
#         label="",
#         empty_label="All positions",
#     )
#     team = forms.ModelChoiceField(
#         required=False,
#         queryset=Team.objects.all(),
#         label="",
#         empty_label="All teams",
#     )


# class TaskTypeSearchForm(forms.Form):
#     name = forms.CharField(
#         max_length=255,
#         required=False,
#         label="",
#         widget=forms.TextInput(attrs={
#             "placeholder": "Search by name",
#         })
#     )


# class PositionSearchForm(forms.Form):
#     name = forms.CharField(
#         max_length=255,
#         required=False,
#         label="",
#         widget=forms.TextInput(attrs={
#             "placeholder": "Search by name",
#         })
#     )


# class ProjectSearchForm(forms.Form):
#     name = forms.CharField(
#         max_length=255,
#         required=False,
#         label="",
#         widget=forms.TextInput(attrs={
#             "placeholder": "Search by name",
#         })
#     )
#     no_tasks = forms.BooleanField(
#         initial=False,
#         required=False,
#         label="No tasks",
#         widget=forms.CheckboxInput()
#     )


# class TeamSearchForm(forms.Form):
#     name = forms.CharField(
#         max_length=255,
#         required=False,
#         label="",
#         widget=forms.TextInput(attrs={
#             "placeholder": "Search by name",
#         })
#     )
#     projects = forms.ModelMultipleChoiceField(
#         required=False,
#         queryset=Project.objects.all(),
#         label="",
#         widget=forms.CheckboxSelectMultiple
#     )
#     no_projects = forms.BooleanField(
#         initial=False,
#         required=False,
#         label="No projects",
#         widget=forms.CheckboxInput()
#     )
#     no_team_members = forms.BooleanField(
#         initial=False,
#         required=False,
#         label="No workers",
#         widget=forms.CheckboxInput()
#     )