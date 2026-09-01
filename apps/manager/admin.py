# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth import get_user_model
#
# from manager.models import Position, Team, Project, TaskType, Task
#
#
# @admin.register(get_user_model())
# class WorkerAdmin(UserAdmin):
#     list_display = UserAdmin.list_display + (
#         "position",
#         "is_manager",
#         "team",
#     )
#     fieldsets = UserAdmin.fieldsets + (
#         (
#             (
#                 "Additional info",
#                 {
#                     "fields": (
#                         "position",
#                         "is_manager",
#                         "team",
#                     )
#                 },
#             ),
#         )
#     )
#     add_fieldsets = UserAdmin.add_fieldsets + (
#         (
#             (
#                 "Additional info",
#                 {
#                     "fields": (
#                         "first_name",
#                         "last_name",
#                         "position",
#                         "is_manager",
#                         "team",
#                     )
#                 },
#             ),
#         )
#     )
#
#
# admin.site.register(Position)
# admin.site.register(Project)
# admin.site.register(Team)
# admin.site.register(TaskType)
# admin.site.register(Task)
