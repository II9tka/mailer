import json
import uuid

from django.apps import apps
from django.db import transaction
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from pytracking.html import adapt_html
from django_celery_beat.models import ClockedSchedule, PeriodicTask, PeriodicTasks

from .utils import get_tracking_configuration


def get_notifies(values):
    model = apps.get_model('notify', model_name='Notify')

    return model.objects.filter(pk__in=values)


def create_periodic_task(notifies, postpone_on):
    with transaction.atomic():
        clocked = ClockedSchedule.objects.create(clocked_time=postpone_on)
        task = PeriodicTask.objects.create(
            clocked=clocked,
            task='notify.tasks.send_mass_html_mail',
            kwargs=json.dumps({"notifies": notifies}),
            one_off=True,
            name=uuid.uuid4()
        )
        PeriodicTasks.changed(task)
    return True


def send_notifies(notifies, connection):
    notifies = get_notifies(notifies)
    messages = []

    for notify in notifies:
        html, subject, text, from_email, recipient = notify.html, notify.subject, notify.text, settings.EMAIL_HOST_USER, notify.email
        html = adapt_html(
            html, extra_metadata={"notify_id": notify.id},
            open_tracking=True, configuration=get_tracking_configuration()
        )
        message = EmailMultiAlternatives(subject, text, from_email, (recipient,))
        message.attach_alternative(html, "text/html")
        messages.append(message)

    return connection.send_messages(messages)
