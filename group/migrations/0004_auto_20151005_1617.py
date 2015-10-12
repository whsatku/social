# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0003_auto_20150921_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupmember',
            name='role',
            field=models.IntegerField(max_length=50),
        ),
    ]
