# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0004_group_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='header',
        ),
        migrations.RemoveField(
            model_name='group',
            name='logo',
        ),
    ]
