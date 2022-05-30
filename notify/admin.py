from django.contrib import admin
from django.contrib.admin import register, ModelAdmin

from solo.admin import SingletonModelAdmin

from .models import Receiver, Notify, Template, Configuration

admin.site.register((Receiver, Template))
admin.site.register(Configuration, SingletonModelAdmin)


@register(Notify)
class NotifyModelAdmin(ModelAdmin):
    readonly_fields = ('delivery_status', 'read_status')
