# -*- coding: UTF-8 -*-
from random import randrange, seed

from django.core.mail import send_mail
# from django.shortcuts import get_object_or_404, render
from rest_framework import mixins, viewsets
# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User

from api_yamdb.settings import ALL_STATUSES

# from .permissions import AuthorEditOrReadAll, AuthorOrReadOnly, ReadOnly
from .serializers import (MailRequestSerializer, UserSerializer,
                          GetTokenSerializer)


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
