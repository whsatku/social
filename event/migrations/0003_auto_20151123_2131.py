# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_auto_20151122_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='end_time',
            field=models.TimeField(default=datetime.datetime(2015, 11, 23, 14, 31, 30, 973000, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='start_time',
            field=models.TimeField(default=datetime.datetime(2015, 11, 23, 14, 31, 37, 820000, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
