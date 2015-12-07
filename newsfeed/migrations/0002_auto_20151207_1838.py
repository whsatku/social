# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsfeed', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='allow_submission',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='pinned',
            field=models.BooleanField(default=False),
        ),
    ]
