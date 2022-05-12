from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Comment, Review, Title
from users.models import User


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
    class Meta:
        fields = (
            'username',
            'confirmation_code',

        )
        model = User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id', 'username', 'first_name',
            'last_name', 'date_joined', 'status'
        )
        model = User
        read_only_fields = ('date_joined',)


class ReviewSerializer(serializers.ModelSerializer):
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
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
