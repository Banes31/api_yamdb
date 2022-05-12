from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.relations import SlugRelatedField
from reviews.models import Token, User


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
