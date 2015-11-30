# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='firstname',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='lastname',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
