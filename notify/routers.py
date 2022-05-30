from rest_framework.routers import DefaultRouter

from .views import NotifyViewSet

router = DefaultRouter()

router.register(r'notify', NotifyViewSet, basename='notify')
