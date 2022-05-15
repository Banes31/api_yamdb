from django.core.exceptions import ValidationError


def my_username_validator(value):
    if value != r'^[\w.@+-]+$' and value == 'me':
        raise ValidationError(
            '%(value)s is not good name',
            params={'value': value},
        )
