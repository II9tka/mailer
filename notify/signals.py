from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask


@receiver(post_save, sender=PeriodicTask)
def delete_one_off_task(sender, instance, created, **kwargs):
    if not created and instance.one_off:
        instance.clocked.delete()
        instance.delete()
