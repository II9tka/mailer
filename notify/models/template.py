from django.template.loader import get_template
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext as _
from django.template import Template as _Template, Context as _Context

from pytracking.html import adapt_html

from .abstracts.notify import AbstractNotify

User = get_user_model()


class Template(AbstractNotify):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True,
        related_name='templates', verbose_name=_('Пользователь')
    )

    def get_template(self, receiver: dict):
        return get_template('notify/index.html').render({'html': _Template(self.html).render(_Context(receiver))})

    def __str__(self):
        return 'Шаблон %s | Пользователь %s' % (self.id, self.user.username,)

    class Meta:
        ordering = ('id',)
        verbose_name = _('Шаблон')
        verbose_name_plural = _('Шаблоны')
