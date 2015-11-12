# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0008_auto_20151109_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 12, 12, 54, 47, 553000, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
