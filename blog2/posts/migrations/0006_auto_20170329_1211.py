# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-29 06:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_author_biography'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='gender',
            field=models.BooleanField(choices=[(True, 'Female'), (False, 'Male')], default=True),
        ),
    ]
