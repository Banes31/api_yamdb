from api.views import UserViewSet
from django.urls import include, path
from rest_framework import routers

from .views import GetTokenViewSet, MailRequestViewSet

# from rest_framework_simplejwt.views import (TokenObtainPairView,
#                                             TokenRefreshView)


router = routers.DefaultRouter()
# router.register('auth', AuthViewSet, basename='auth')
router.register('users', UserViewSet, basename='users')
router.register('auth/signup', MailRequestViewSet, basename='signup')
router.register('auth/token', GetTokenViewSet, basename='token')


urlpatterns = [
    # path(
    #     'v1/auth/token/',
    #     TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path(
    #     'v1/token/refresh/',
    #     TokenRefreshView.as_view(), name='token_refresh'),
    # path('v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('v1/', include(router.urls)),
]
