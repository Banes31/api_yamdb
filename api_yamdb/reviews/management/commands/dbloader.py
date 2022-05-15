import csv

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    GenreTitle,
    Title,
    User
)


class Command(BaseCommand):
    """
    Management-Command для загрузки данных
    в БД из csv файлов из каталога /static/data .
    """
    help = ('Заполенение БД тестовыми данными из csv  '
            'файлов из каталога "/api_yamdb/static/data" '
            'Если таблицы не пустые, то загрузка пропускается.')

    def load_to_users_table(self):
        """Заполнение таблицы с пользователями."""
        try:
            with open('static/data/users.csv', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row_num, row in enumerate(reader):
                    if row_num == 0:
                        continue
                    else:
                        User.objects.get_or_create(
                            id=row[0],
                            username=row[1],
                            email=row[2],
                            role=row[3],
                            bio=row[4],
                            first_name=row[5],
                            last_name=row[6],
                        )
            return self.stdout.write('Загруженно без ошибок.')
        except Exception as error:
            self.stderr.write('При загрузки возникла ошибка:')
            raise Exception(error)
        finally:
            csvfile.close()

    def load_to_category_table(self):
        """Заполнение таблицы с категориями."""
        try:
            with open('static/data/category.csv', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row_num, row in enumerate(reader):
                    if row_num == 0:
                        continue
                    else:
                        Category.objects.get_or_create(
                            id=row[0],
                            name=row[1],
                            slug=row[2]
                        )
            return self.stdout.write('Загруженно без ошибок.')
        except Exception as error:
            self.stderr.write('При загрузки возникла ошибка:')
            raise Exception(error)
        finally:
            csvfile.close()

    def load_to_titles_table(self):
        """Заполнение таблицы произведений."""
        try:
            with open('static/data/titles.csv', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row_num, row in enumerate(reader):
                    if row_num == 0:
                        continue
                    else:
                        if Title.objects.filter(id=row[0]).exists():
                            continue
                        Title.objects.get_or_create(
                            id=row[0],
                            name=row[1],
                            year=row[2],
                            category=get_object_or_404(Category, id=row[3])
                        )
            return self.stdout.write('Загруженно без ошибок.')
        except Exception as error:
            self.stderr.write('При загрузки возникла ошибка:')
            raise Exception(error)
        finally:
            csvfile.close()

    def load_to_reviews_table(self):
        """Заполнение таблицы с отзывами."""
        try:
            with open('static/data/review.csv', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row_num, row in enumerate(reader):
                    if row_num == 0:
                        continue
                    else:
                        if Review.objects.filter(id=row[0]).exists():
                            continue
                        Review.objects.get_or_create(
                            id=row[0],
                            title_id=row[1],
                            text=row[2],
                            author=get_object_or_404(User, id=row[3]),
                            score=row[4],
                            pub_date=row[5]
                        )
            return self.stdout.write('Загруженно без ошибок.')
        except Exception as error:
            self.stderr.write('При загрузки возникла ошибка:')
            raise Exception(error)
        finally:
            csvfile.close()

    def load_to_genre_table(self):
        """Заполнение таблицы жанров."""
        try:
            with open('static/data/genre.csv', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row_num, row in enumerate(reader):
                    if row_num == 0:
                        continue
                    else:
                        Genre.objects.get_or_create(
                            id=row[0],
                            name=row[1],
                            slug=row[2]
                        )
            return self.stdout.write('Загруженно без ошибок.')
        except Exception as error:
            self.stderr.write('При загрузки возникла ошибка:')
            raise Exception(error)
        finally:
            csvfile.close()

    def load_to_genre_title_table(self):
        """Заполнение таблицы с жанрами - произведениями."""
        try:
            with open(
                'static/data/genre_title.csv', encoding='utf-8'
            ) as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row_num, row in enumerate(reader):
                    if row_num == 0:
                        continue
                    else:
                        GenreTitle.objects.get_or_create(
                            id=row[0],
                            title_id=get_object_or_404(Title, id=row[1]),
                            genre_id=get_object_or_404(Genre, id=row[2])
                        )
            return self.stdout.write('Загруженно без ошибок.')
        except Exception as error:
            self.stderr.write('При загрузки возникла ошибка:')
            raise Exception(error)
        finally:
            csvfile.close()

    def load_to_comments_table(self):
        """Заполнение таблицы комментариев."""
        try:
            with open('static/data/comments.csv', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row_num, row in enumerate(reader):
                    if row_num == 0:
                        continue
                    else:
                        if Comment.objects.filter(id=row[0]).exists():
                            continue
                        Comment.objects.get_or_create(
                            id=row[0],
                            review_id=get_object_or_404(Review, id=row[1]),
                            text=row[2],
                            author=get_object_or_404(User, id=row[3]),
                            pub_date=row[4]
                        )
            return self.stdout.write('Загруженно без ошибок.')
        except Exception as error:
            self.stderr.write('При загрузки возникла ошибка:')
            raise Exception(error)
        finally:
            csvfile.close()

    def handle(self, *args, **options):
        try:
            self.load_to_users_table()
            self.load_to_category_table()
            self.load_to_titles_table()
            self.load_to_reviews_table()
            self.load_to_genre_table()
            # self.load_to_genre_title_table()
            self.load_to_comments_table()
        except Exception as error:
            self.stderr.write(f'Возникла ошибка: {error}')
