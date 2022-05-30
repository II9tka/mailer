from django.db import models
from django.utils.translation import ugettext as _

from ...validators import validate_html


class AbstractNotify(models.Model):
    text = models.TextField(
        verbose_name=_('Текст')
    )
    subject = models.CharField(
        max_length=128, default='', verbose_name=_('Заголовок')
    )
    html = models.TextField(
        verbose_name=_('HTML'), max_length=5000, validators=[validate_html]
    )

    class Meta:
        abstract = True
