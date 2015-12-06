# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_auto_20151130_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='firstname',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
    ]
