# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-31 07:22
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20170329_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='photo',
            field=models.ImageField(null=True, upload_to=django.core.files.storage.FileSystemStorage(location='/media/author_photo')),
        ),
    ]
