from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def add_user_to_manager_groups(sender, instance, created, **kwargs):
    """function to add superuser to manager group by default"""
    if instance.is_superuser:
        instance.groups.add(Group.objects.get(name="Manager"))
        instance.is_manager = True
