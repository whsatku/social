# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_userprofile_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='faculty',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(max_length=5, null=True, choices=[(b'M', b'Male'), (b'F', b'Female')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='major',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='types',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
