from rest_framework import serializers
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
