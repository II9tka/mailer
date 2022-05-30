from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext as _

from django_fsm import FSMField, transition

from .abstracts.notify import AbstractNotify
from ..tasks import send_mass_html_mail
from ..models import Template

User = get_user_model()


class Notify(AbstractNotify):
    class DeliveryStatus(models.TextChoices):
        WAIT = '0', 'Ожидает'
        DELIVERED = '1', 'Доставлено'
        REJECTED = '2', 'Отклонено'

    class ReadStatus(models.TextChoices):
        UNREAD = '0', 'Не прочитано'
        READ = '1', 'Прочитано'

    delivery_status = FSMField(
        choices=DeliveryStatus.choices, verbose_name=_('Состояние доставки'),
        default=DeliveryStatus.WAIT, protected=True, editable=False
    )
    read_status = FSMField(
        choices=ReadStatus.choices, verbose_name=_('Состояние прочтения'),
        default=ReadStatus.UNREAD, protected=True, editable=False
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='notifies', verbose_name=_('Пользователь')
    )
    email = models.EmailField(
        max_length=255, blank=True, null=True, verbose_name=_('Почта получателя')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Дата создания')
    )
    postpone_on = models.DateTimeField(
        null=True, blank=True, default=None, verbose_name=_('')
    )

    def is_read(self):
        return self.read_status == self.ReadStatus.READ

    def get_email_args(self) -> tuple:
        return self.subject, self.text, self.html, settings.EMAIL_HOST_USER, self.email

    @classmethod
    def create(cls, user: User, template: Template, postpone_on: datetime = None) -> bool:
        notifies = cls.objects.bulk_create(cls(
            text=template.text,
            subject=template.subject,
            html=template.get_template(receiver),
            user=user,
            email=receiver['email'],
            postpone_on=postpone_on
        ) for receiver in user.receivers.values())

        # send_mass_html_mail.delay(notifies=[n.pk for n in notifies], postpone_on=str(postpone_on))
        send_mass_html_mail(notifies=[n.pk for n in notifies], postpone_on=str(postpone_on))

        return True

    @transition(field=delivery_status, source=DeliveryStatus.WAIT, target=DeliveryStatus.DELIVERED)
    def delivered(self): ...

    @transition(field=delivery_status, source=DeliveryStatus.WAIT, target=DeliveryStatus.REJECTED)
    def rejected(self): ...

    @transition(field=read_status, source=ReadStatus.UNREAD, target=ReadStatus.READ)
    def read(self): ...

    def __str__(self):
        return 'Кому %s | От %s' % (self.email, self.user.username,)

    class Meta:
        ordering = ('id',)
        verbose_name = _('Письмо')
        verbose_name_plural = _('Письма')
