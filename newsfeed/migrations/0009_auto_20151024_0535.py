# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsfeed', '0008_auto_20151007_0452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='target_id',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
