# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsfeed', '0002_auto_20151207_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='file',
            field=models.FileField(
                upload_to=lambda instance, filename: 'posts/{0}_{1}'.format(instance.id, filename),
                null=True
            ),
        ),
    ]
