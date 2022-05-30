from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext as _


class User(AbstractUser):
    ...

    class Meta:
        ordering = ('id',)
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
