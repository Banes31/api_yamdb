# Generated by Django 2.2.16 on 2022-05-14 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_genretitle'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-pub_date', '-review_id', '-id'), 'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='review',
            new_name='review_id',
        ),
    ]