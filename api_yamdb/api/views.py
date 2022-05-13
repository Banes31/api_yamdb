from random import randrange, seed

from django.core.mail import send_mail
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Review, Title, User

from .permissions import (AdminOnly, AuthorEditOrReadAll, AuthorOrReadOnly,
                          ReadOnly)
from .serializers import (CommentSerializer, GetTokenSerializer, MeSerializer,
                          ReviewSerializer, SignUpSerializer, UsersSerializer)

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


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзыва."""
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
    """Вьюсет для комментария."""
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
