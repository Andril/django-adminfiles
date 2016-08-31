# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminfiles', '0002_auto_20160731_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='description',
            field=models.CharField(max_length=200, blank=True, verbose_name='подпись к файлу'),
        ),
    ]
