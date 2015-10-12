# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0006_auto_20151005_2202'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='long_description',
            new_name='activities',
        ),
        migrations.AddField(
            model_name='group',
            name='category',
            field=models.CharField(default=1, max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='group',
            name='short_description',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='group',
            name='description',
            field=models.CharField(max_length=200),
        ),
    ]
