# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsfeed', '0007_auto_20151007_0329'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='date',
            new_name='datetime',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='date',
            new_name='datetime',
        ),
    ]
