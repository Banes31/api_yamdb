from api.filters import TitleFilter
from api.utils import code_gen
from api_yamdb.settings import EMAIL_FROM
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Review, Title, User

from .mixins import CustomViewSet
from .permissions import (
    AdminOnly,
    IsAdminOrReadOnly,
    IsAuthorOrAdminOrModeratorOrReadOnly
)
from .serializers import (
    AdminSerializer,
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    GetTokenSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    UsersSerializer
)


class SignUp(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get_or_create(
            username=request.data['username'],
            email=request.data['email']
        )[0]
        user.confirmation_code = code_gen()
        if not request.user.is_superuser:
            send_mail(
                u'Код подтверждения для YAMDB',
                u'Сделайте POST запрос '
                f'"username": "{user.username}", '
                f'"confirmation_code": "{user.confirmation_code}" '
                u'на http://127.0.0.1:8000/api/v1/auth/token/',
                EMAIL_FROM,
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
    serializer_class = AdminSerializer
    permission_classes = (AdminOnly, IsAuthenticated)
    lookup_field = 'username'

    def perform_create(self, serializer):
        serializer.save(confirmation_code=code_gen())

    @action(
        methods=['GET', 'PATCH'], detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated],
    )
    def user_info(self, request):
        serializer = AdminSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.role == 'admin':
                serializer = AdminSerializer(
                    request.user, data=request.data, partial=True)
            else:
                serializer = UsersSerializer(
                    request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class CategoryViewSet(CustomViewSet):
    """Вьюсет для обработки к эндпоинту category/."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(CustomViewSet):
    """Вьюсет для обработки запросов к эндпоинту genre/."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки CRUD запросов к эндпоинту title/."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ('name', )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзыва."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminOrModeratorOrReadOnly,
    )

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
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminOrModeratorOrReadOnly,
    )

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs['review_id']
        )

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(
            author=self.request.user,
            review_id=review
        )

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()
