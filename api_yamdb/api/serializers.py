from asyncio.windows_events import NULL
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title, User


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для создания аккаунта в модели user."""
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        fields = (
            'email',
            'username',
        )
        model = User

    def validate(self, data):
        """Проверка username на me."""
        if self.initial_data['username'] == '':
            raise serializers.ValidationError('Это поле не может быть пустым!')
        if self.initial_data['username'] == 'me':
            raise serializers.ValidationError('Нельзя использовать me!')
        if User.objects.filter(username=self.initial_data['username']):
            raise serializers.ValidationError('Такой username уже есть!')
        if self.initial_data['email'] is NULL:
            raise serializers.ValidationError('Это поле не может быть пустым!')
        if User.objects.filter(email=self.initial_data['email']):
            raise serializers.ValidationError('Такой email уже есть!')
        return data


class GetTokenSerializer(serializers.ModelSerializer):
    """Сериализатор получения токена, модель user."""
    username = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('username', 'confirmation_code', 'token')
        model = User

    def validate(self, data):
        """Проверка валидности полей."""
        if 'username' not in self.initial_data:
            raise ValidationError()
        find_user = get_object_or_404(
            User, username=self.initial_data['username'])
        if (
            not find_user.is_superuser and (
                find_user.confirmation_code != self.initial_data[
                    'confirmation_code'
                ]
            )
        ):
            raise ValidationError()
        return super().validate(data)


class AdminSerializer(serializers.ModelSerializer):
    """Сериализатор для админа, модель users."""
    class Meta:
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        model = User


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели отзыва."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        """Проверка чтобы пользователь не мог добавить более одного отзыва."""
        title = self.context['view'].kwargs.get('title_id')
        user = self.context['request'].user
        if self.context['request'].method == 'POST':
            if Review.objects.filter(
                title=title,
                author=user,
                title__id=self.context['view'].kwargs.get('title_id')
            ).exists():
                raise serializers.ValidationError(
                    'Нельзя добавлять более одного отзыва!'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментария."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)


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

    def validate_year(self, value):
        """Проверка, что год выпуска не может быть больше текущего."""
        now = timezone.now().year
        if value > now:
            raise ValidationError(
                f'Год выпуска {value} не может быть больше текущего {now}!'
            )
        if value is None:
            raise ValidationError('Год выпуска обязателен для заполнения!')
        return value


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор для обычного пользователя в users"""
    class Meta:
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        model = User
        read_only_fields = ('role',)
