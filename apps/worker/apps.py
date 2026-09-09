from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_manager_group(sender, **kwargs):
    """function to create manager group with migration"""
    from django.contrib.auth.models import Group, Permission

    manager_group, _ = Group.objects.get_or_create(name="Manager")
    perms = Permission.objects.filter(
        codename__in=[
            "add_task",
            "delete_task",
            "add_position",
            "change_position",
            "delete_position",
            "add_project",
            "change_project",
            "delete_project",
            "add_team",
            "change_team",
            "delete_team",
            "add_worker",
            "change_worker",
            "delete_worker",
            "add_tasktype",
            "change_tasktype",
            "delete_tasktype",
        ]
    )
    manager_group.permissions.set(perms)


class WorkerConfig(AppConfig):
    name = "apps.worker"

    def ready(self):
        import apps.worker.signals
        post_migrate.connect(create_manager_group, sender=self)
