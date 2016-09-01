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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=150, verbose_name='название')),
                ('slug', models.SlugField(max_length=150, unique=True, verbose_name='slug')),
                ('description', models.CharField(blank=True, max_length=200, verbose_name='подпись к галлерее')),
            ],
            options={
                'verbose_name_plural': 'галереи',
                'verbose_name': 'галерея',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='ImageForGallery',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=300, verbose_name='название')),
                ('image', models.ImageField(upload_to=adminfiles.models.get_photo_path, verbose_name='фото')),
                ('show_order', models.PositiveIntegerField(db_index=True, default=0, verbose_name='порядковый номер вывода')),
                ('gallery', models.ForeignKey(related_name='galleryimages', verbose_name='галерея', to='adminfiles.Gallery')),
            ],
            options={
                'verbose_name_plural': 'фото для галерей',
                'verbose_name': 'фото для галереи',
                'ordering': ['title'],
            },
        ),
    ]
