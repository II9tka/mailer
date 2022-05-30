from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext as _

User = get_user_model()


class Receiver(models.Model):
    first_name = models.CharField(
        max_length=128, verbose_name=_('Имя')
    )
    last_name = models.CharField(
        max_length=128, verbose_name=_('Фамилия')
    )
    email = models.EmailField(
        max_length=128, verbose_name=_('Почта')
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='receivers', help_text=_(
            'Пользователь, создавший получателя.'
        ),
        verbose_name=_('Пользователь')
    )

    def get_full_name(self):
        return '%s %s'.strip() % (self.first_name, self.last_name,)

    def __str__(self):
        return self.first_name

    class Meta:
        ordering = ('id',)
        verbose_name = _('Получатель')
        verbose_name_plural = _('Получатели')
