from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Comment, Review, Title
from users.models import User
from rest_framework.exceptions import NotFound
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Genre, Title, Token, User


class ChoicesField(serializers.Field):
    def __init__(self, choices, **kwargs):
        self._choices = choices
        super(ChoicesField, self).__init__(**kwargs)

    def to_representation(self, obj):
        return self._choices[obj]

    def to_internal_value(self, data):
        return getattr(self._choices, data)


class MailRequestSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'email',
            'username',
        )
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Нельзя использовать me!')
        return value


class GetTokenSerializer(serializers.ModelSerializer):
    username = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('username', 'confirmation_code', 'token')
        model = Token

    def validate(self, data):
        find_users = User.objects.filter(
            username=self.initial_data['username'],
            confirmation_code=self.initial_data['confirmation_code'])
        if find_users:
            find_tokens = Token.objects.filter(
                username=find_users[0])
        print(find_users)
        if not find_users:
            raise NotFound('Пользователь не найден')
        if find_tokens:
            raise serializers.ValidationError('Токен уже есть!')
        return super().validate(data)

    def to_representation(self, instance):
        return {'token': instance.token}


class UsersSerializer(serializers.ModelSerializer):
    role = ChoicesField(choices=User.ALL_STATUSES)

    class Meta:
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        model = User


class MeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio'
        )
        model = User
        read_only_fields = ('date_joined',)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели отзыва"""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        """Проверка чтобы пользователь не мог добавить более одного отзыва."""
        request = self.context.get('request')
        if request.method != 'POST':
            return data
        user = None
        if request and hasattr(request, 'user'):
            user = request.user
        kwargs = request.parser_context.get('kwargs')
        title_id = kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_exist = Review.objects.filter(
            author=user,
            title=title
        ).exists()
        if review_exist:
            raise serializers.ValidationError(
                'Нельзя добавлять более одного отзыва!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментария"""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        exclude = ('id', )
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        exclude = ('id', )
        model = Genre
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title - только чтение."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title - чтение и запись."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title
