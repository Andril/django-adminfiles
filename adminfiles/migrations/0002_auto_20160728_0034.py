# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import adminfiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('adminfiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileupload',
            name='form_field',
            field=models.CharField(null=True, blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='fileupload',
            name='upload',
            field=models.FileField(verbose_name='file', upload_to=adminfiles.models.get_photo_path),
        ),
    ]

