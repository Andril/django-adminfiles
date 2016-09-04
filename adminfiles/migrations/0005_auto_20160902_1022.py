# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminfiles', '0004_gallery_imageforgallery'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imageforgallery',
            options={'ordering': ['show_order'], 'verbose_name_plural': 'фото для галерей', 'verbose_name': 'фото для галереи'},
        ),
        migrations.RemoveField(
            model_name='imageforgallery',
            name='title',
        ),
    ]
