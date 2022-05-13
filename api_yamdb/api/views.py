# -*- coding: UTF-8 -*-
from random import randrange, seed
from rest_framework import status
from django.core.mail import send_mail
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from reviews.models import User

from .permissions import (AuthorEditOrReadAll, AuthorOrReadOnly, ReadOnly,
                          AdminOnly)
from .serializers import (GetTokenSerializer, SignUpSerializer,
                          MeSerializer, UsersSerializer)

MIN_VALUE_CODE = 100000
MAX_VALUE_CODE = 999999


def code_gen():
    seed()
    return str(randrange(MIN_VALUE_CODE, MAX_VALUE_CODE))


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass


class UpdateViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    pass


class SignUp(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_set = User.objects.filter(
            username=request.data['username'],
            email=request.data['email']
        )
        if user_set:
            user = user_set[0]
        else:
            # serializer.is_valid(raise_exception=True)
            user = serializer.save(
                confirmation_code=code_gen(),
            )
        if not request.user.is_superuser:
            send_mail(
                u'Код подтверждения для YAMDB',
                u'Сделайте POST запрос '
                f'"username": "{user.username}", '
                f'"confirmation_code": "{user.confirmation_code}" '
                u'на http://127.0.0.1:8000/api/v1/auth/token/',
                'from@yamdb.com',
                [f'{user.email}'],
                fail_silently=False,
            )
        return Response(
            {
                "username": f"{user.username}",
                "email": f"{user.email}"
            },
            status=status.HTTP_200_OK
        )


class Token(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
            serializer = GetTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = get_object_or_404(User, username=request.data['username'])
            if not user.is_superuser:
                user = get_object_or_404(
                    User, username=request.data['username'],
                    confirmation_code=request.data['confirmation_code']
                )
            else:
                user.role = 'admin'
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            user.token = token
            user.save()
            return Response(
                {"token": f"{user.token}"}, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (AdminOnly, )

    def perform_create(self, serializer):
        serializer.save(confirmation_code=code_gen())

    # def get_permissions(self):
    #     if self.action == 'retrieve':
    #         return (ReadOnly(),)
    #     return super().get_permissions()


class Me(APIView):
    permission_classes = (AllowAny, )
    
    def update(self, request):
        return ()

    # @action(detail=False, methods=['post'], url_path='me')
    # def perform_update(self, serializer):
    #     # user = get_object_or_404(User, pk=self.request.user)
    #     serializer.save(
    #         username=serializer.initial_data['username'],
    #         email=serializer.initial_data['email'],
    #         first_name=serializer.initial_data['first_name'],
    #         last_name=serializer.initial_data['last_name'],
    #         bio=serializer.initial_data['bio']
    #     )
