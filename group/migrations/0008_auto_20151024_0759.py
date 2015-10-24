# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0007_auto_20151012_0929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='permisssion',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='group',
            name='type',
            field=models.IntegerField(),
        ),
    ]
