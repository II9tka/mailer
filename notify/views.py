from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import NotifySerializer


class NotifyViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['POST'])
    def update_read_status(self, request):
        serializer = NotifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'success', 'status': status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
