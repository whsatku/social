# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0003_auto_20151123_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='parent',
            field=models.ForeignKey(related_name='children', blank=True, to='group.Group', null=True),
        ),
    ]
