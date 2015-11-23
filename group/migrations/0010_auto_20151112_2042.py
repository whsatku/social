# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0009_group_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
