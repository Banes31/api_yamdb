from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Category(models.Model):
    """Модель категории."""
    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField('Slug категории', unique=True)

    def __str__(self):
        return f'{self.name} {self.slug}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    """Модель жанра."""
    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField('Slug жанра', unique=True)

    def __str__(self):
        return f'{self.name} {self.slug}'

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведения."""
    name = models.CharField('Название произведения', max_length=256)
    year = models.PositiveSmallIntegerField(
        'Год выпуска произведения',
        min_length=4,
        max_length=4
    )
    description = models.TextField(
        'Описание произведения',
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Жанр',
    )

    def __str__(self):
        return self.name[:15]

    class Meta:
        ordering = ('-year')
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


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
    review = models.ForeignKey(
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
        ordering = ('-pub_date', '-review', '-id',)