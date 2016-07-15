# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('upload_date', models.DateTimeField(auto_now_add=True, verbose_name='upload date')),
                ('upload', models.FileField(verbose_name='file', upload_to='adminfiles')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='slug')),
                ('description', models.CharField(max_length=200, verbose_name='description', blank=True)),
                ('content_type', models.CharField(max_length=100, editable=False)),
                ('sub_type', models.CharField(max_length=100, editable=False)),
            ],
            options={
                'verbose_name_plural': 'file uploads',
                'ordering': ['upload_date', 'title'],
                'verbose_name': 'file upload',
            },
        ),
        migrations.CreateModel(
            name='FileUploadReference',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('upload', models.ForeignKey(to='adminfiles.FileUpload')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='fileuploadreference',
            unique_together=set([('upload', 'content_type', 'object_id')]),
        ),
    ]
