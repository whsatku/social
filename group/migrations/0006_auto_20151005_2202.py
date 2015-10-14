# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0005_auto_20151005_2156'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groupmember',
            old_name='group_id',
            new_name='group',
        ),
        migrations.RenameField(
            model_name='groupmember',
            old_name='user_id',
            new_name='user',
        ),
    ]
