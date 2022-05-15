from django.contrib.auth.models import AbstractUser
from .validators import my_username_validator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from model_utils import Choices


class User(AbstractUser):
    """Модель юзера."""

    ALL_STATUSES = Choices(
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        help_text=(
            "Required. 150 char or fewer. Letters, and digits only."
        ),
        validators=[my_username_validator]
    )
    role = models.CharField(
        verbose_name='Роль пользователя',
        max_length=16,
        choices=ALL_STATUSES,
        default='user',
        blank=True
    )
    first_name = models.CharField(
        verbose_name='Имя', max_length=150, blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия', max_length=150, blank=True
    )
    email = models.EmailField(
        verbose_name='email', unique=True, max_length=254
    )
    bio = models.TextField(
        verbose_name='Биография', blank=True
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=6,
        blank=True
    )
    token = models.TextField(
        verbose_name='токен', blank=True)

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    """Модель категории."""
    name = models.CharField(verbose_name='Название категории', max_length=256)
    slug = models.SlugField(verbose_name='Slug категории', unique=True)

    def __str__(self):
        return f'{self.name} {self.slug}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    """Модель жанра."""
    name = models.CharField(verbose_name='Название жанра', max_length=256)
    slug = models.SlugField(verbose_name='Slug жанра', unique=True)

    def __str__(self):
        return f'{self.name} {self.slug}'

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведения."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения'
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска произведения')
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание произведения'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )

    def __str__(self):
        return self.name[:15]

    class Meta:
        ordering = ('name', '-year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        indexes = [
            models.Index(fields=['year'], name='year_idx'),
        ]


class GenreTitle(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Произведение'
    )
    genre_id = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        related_name='genres',
        verbose_name='Жанр'
    )


class Review(models.Model):
    """Модель отзыва."""
    title = models.ForeignKey(
        to=Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Название произведения'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка произведения',
        validators=(
            MaxValueValidator(
                10, 'Максимальная оценка <= 10.'),
            MinValueValidator(
                1, 'Минимальная оценка >= 1.'),
        ),
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата отзыва'
    )

    def __str__(self):
        return f'{str(self.author)}: {str(self.score)} - {str(self.title)}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date', 'title', '-score', 'text')
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_review'),
        )


class Comment(models.Model):
    """Модель комментария к отзыву."""
    review_id = models.ForeignKey(
        to=Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата комментария'
    )

    def __str__(self):
        return f'{self.author}: {self.text[:15]}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date', '-review_id', '-id',)
