# Generated by Django 2.2.16 on 2022-05-14 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20220514_1441'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
    ]