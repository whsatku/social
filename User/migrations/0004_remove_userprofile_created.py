# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_userprofile_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='created',
        ),
    ]
