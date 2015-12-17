# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsfeed', '0004_auto_20151208_0511'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='target_name',
            field=models.CharField(max_length=20000, null=True),
        ),
    ]
