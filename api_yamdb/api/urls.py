from django.urls import include, path
from rest_framework import routers

from .views import (
  CategoryViewSet,
  CommentViewSet,
  GenreViewSet,
  ReviewViewSet,
  SignUp,
  TitleViewSet,
  Token,
  UsersViewSet
)

router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignUp.as_view(), name='signup'),
    path('v1/auth/token/', Token.as_view(), name='token'),
]
