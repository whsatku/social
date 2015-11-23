# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0002_auto_20151123_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='category',
            field=models.ForeignKey(to='group.GroupCategory', null=True),
        ),
    ]
