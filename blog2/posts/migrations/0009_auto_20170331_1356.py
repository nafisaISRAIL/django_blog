# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-31 07:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_author_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='photo',
            field=models.ImageField(null=True, upload_to='author_photo'),
        ),
    ]
