# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-05 14:20
from __future__ import unicode_literals

from django.db import migrations


def migrate_authors(apps, schema_editor):
    from django.contrib.auth import get_user_model
    Author = apps.get_model('posts', 'Author')
    User = get_user_model()
    for a in Author.objects.all():
        u = User(username=a.email,
                 first_name=a.first_name, last_name=a.last_name,
                 email=a.email)
        u.set_password('123456789')
        u.save()
        a.user_id = u
        a.save()


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0016_author_user'),
    ]

    operations = [
        migrations.RunPython(migrate_authors)
    ]
