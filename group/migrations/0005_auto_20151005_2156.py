# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0004_auto_20151005_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupmember',
            name='role',
            field=models.IntegerField(),
        ),
    ]
