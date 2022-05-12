from django.contrib.auth.models import AbstractUser
from django.db import models
from model_utils import Choices


class User(AbstractUser):
    ALL_STATUSES = Choices(
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=1,
        choices=ALL_STATUSES,
        default='user',
    )
    first_name = models.CharField('first name', max_length=150, blank=True)
    last_name = models.CharField('first name', max_length=150, blank=True)
    email = models.EmailField('email', unique=True, max_length=254)
    bio = models.TextField('Биография', blank=True)
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=6,
    )


class Token(models.Model):
    username = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='tokens')
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=6,
    )
    token = models.TextField('токен', blank=True)

    def __str__(self):
        return self.token
