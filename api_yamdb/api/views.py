# -*- coding: UTF-8 -*-
from random import randrange, seed
from rest_framework.pagination import LimitOffsetPagination
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
# from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User

from api_yamdb.settings import ALL_STATUSES

from reviews.models import Review, Comment, Title
from api.serializers import (
    ReviewSerializer,
    CommentSerializer,
    MailRequestSerializer,
    GetTokenSerializer,
    UserSerializer,
)
from api.permissions import (
    AuthorEditOrReadAll,
    AuthorOrReadOnly,
    ReadOnly
)

MIN_VALUE_CODE = 100000
MAX_VALUE_CODE = 999999


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass


class MailRequestViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = MailRequestSerializer
    permission_classes = (AllowAny, )

    def perform_create(self, serializer):
        seed()
        code = str(randrange(MIN_VALUE_CODE, MAX_VALUE_CODE))
        serializer.save(
            username=serializer.initial_data['username'],
            email=serializer.initial_data['email'],
            confirmation_code=code,
            role=ALL_STATUSES[0])
        send_mail(
            u'Код подтверждения для YAMDB',
            u'Сделайте POST запрос '
            f'"username": "{serializer.initial_data["username"]}", '
            f'"confirmation_code": "{code}" '
            u'на http://127.0.0.1:8000/api/v1/auth/token/',
            'from@yamdb.com',
            [f'{serializer.initial_data["email"]}'],
            fail_silently=False,
        )


class GetTokenViewSet(CreateViewSet):
    queryset = User.objects.filter(
        username='username',
        confirmation_code='confirmation_code')
    serializer_class = GetTokenSerializer
    permission_classes = (AllowAny, )

    def perform_create(self, serializer):
        if not self.queryset:
            raise ('Пользователь не найден')
        return super().perform_create(serializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (AuthorEditOrReadAll, )

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

    # def get_permissions(self):
    #     if self.action == 'retrieve':
    #         return (ReadOnly(),)
    #     return super().get_permissions()


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AuthorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(
            author=self.request.user,
            title=title
        )

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs['review_id'],
            title__id=self.kwargs['title_id']
        )

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(
            author=self.request.user,
            review=review
        )

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()
