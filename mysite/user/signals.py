import os
from django.dispatch import receiver
from django.db import models
from user.models import User


@receiver(models.signals.post_delete, sender=User)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes photo of User when user object is deleted
    """
    if instance.photo:
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)


@receiver(models.signals.pre_save, sender=User)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old photo of user when the photo is updated with new file
    """
    if not instance.pk:
        return False

    try:
        old_photo = User.objects.get(pk=instance.pk).photo
    except User.DoesNotExist:
        return False

    new_photo = instance.photo
    if not old_photo == new_photo:
        if os.path.isfile(old_photo.path):
            os.remove(old_photo.path)
