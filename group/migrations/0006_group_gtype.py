# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0005_auto_20151130_2131'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='gtype',
            field=models.IntegerField(default=0),
        ),
    ]
