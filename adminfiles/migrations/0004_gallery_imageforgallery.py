# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import adminfiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('adminfiles', '0003_auto_20160831_0912'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=150, verbose_name='название')),
                ('slug', models.SlugField(unique=True, max_length=150, verbose_name='slug')),
                ('form_field', models.CharField(max_length=200, verbose_name='поле формы', blank=True, null=True)),
                ('description', models.CharField(max_length=200, verbose_name='подпись к галерее', blank=True)),
            ],
            options={
                'verbose_name': 'галерея',
                'verbose_name_plural': 'галереи',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='ImageForGallery',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('image', models.ImageField(verbose_name='фото', upload_to=adminfiles.models.get_photo_path)),
                ('show_order', models.PositiveIntegerField(db_index=True, verbose_name='порядковый номер вывода', default=1)),
                ('gallery', models.ForeignKey(verbose_name='галерея', to='adminfiles.Gallery', related_name='galleryimages')),
            ],
            options={
                'verbose_name': 'фото для галереи',
                'verbose_name_plural': 'фото для галерей',
                'ordering': ['show_order'],
            },
        ),
    ]
