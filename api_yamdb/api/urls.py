from django.urls import include, path
from rest_framework import routers

from .views import (
    CategoryViewSet,
    GenreViewSet,
    Me,
    SignUp,
    Token,
    UsersViewSet,
    TitleViewSet,
)

router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='users')
# router.register('users/me', MeViewSet, basename='me')
# router.register('auth/signup', SignUpView, basename='signup')
# router.register('auth/token', GetTokenViewSet, basename='token')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignUp.as_view(), name='signup'),
    path('v1/auth/token/', Token.as_view(), name='token'),
    path('v1/users/me/', Me.as_view(), name='me')
]
