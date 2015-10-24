# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_auto_20151019_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='target_id',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
