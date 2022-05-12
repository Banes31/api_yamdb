from django.urls import include, path
from rest_framework import routers

from .views import GetTokenViewSet, MailRequestViewSet, MeViewSet, UsersViewSet


router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='users')
router.register('users/me', MeViewSet, basename='me')
router.register('auth/signup', MailRequestViewSet, basename='signup')
router.register('auth/token', GetTokenViewSet, basename='token')


urlpatterns = [
    path('v1/', include(router.urls)),
]
