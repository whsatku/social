# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_auto_20151027_0110'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='created',
            field=models.BooleanField(default=False),
        ),
    ]
