from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb.settings import ALL_STATUSES


class User(AbstractUser):
    role = models.CharField(
        'Роль пользователя',
        max_length=16,
        choices=ALL_STATUSES,
        default='u'
    )
    email = models.EmailField('email', unique=True)
    bio = models.TextField('Биография', blank=True)
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=6,
    )
