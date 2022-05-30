from typing import List

from django.core.mail import get_connection

from celery import shared_task
from celery.utils.log import get_task_logger

from .services import create_periodic_task, send_notifies

logger = get_task_logger(__name__)


@shared_task
def send_mass_html_mail(notifies: List[int] = None, postpone_on: str = None, fail_silently=False, user=None,
                        password=None, connection=None):
    connection = connection or get_connection(
        username=user, password=password, fail_silently=fail_silently
    )

    if postpone_on is not None:
        return create_periodic_task(notifies, str(postpone_on))
    else:
        return send_notifies(notifies, connection)
