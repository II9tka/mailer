from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Notify


class NotifySerializer(serializers.Serializer):
    is_open_tracking = serializers.BooleanField(write_only=True)
    is_click_tracking = serializers.BooleanField(write_only=True)
    metadata = serializers.JSONField(write_only=True)
    request_data = serializers.JSONField(write_only=True)
    timestamp = serializers.IntegerField(write_only=True)
    result = serializers.JSONField(read_only=True)

    def validate_metadata(self, value):
        if value.get('notify_id'):
            return value
        raise ValidationError('notify_id is required')

    def create(self, validated_data):
        notify_id = validated_data['metadata']['notify_id']

        try:
            notify = Notify.objects.get(id=notify_id)
        except Notify.DoesNotExist:
            raise ValidationError({'notify': '%s does not exist.' % Notify.__name__})

        if notify.is_read():
            raise ValidationError({'notify': 'Notify is read.'})

        notify.read()
        notify.save()

        return {'result': 'Success'}
