from rest_framework.routers import DefaultRouter

from .views import ContactViewSet, UserViewSet

router = DefaultRouter()
router.register('contacts', ContactViewSet, base_name='contacts')
router.register('users', UserViewSet)
