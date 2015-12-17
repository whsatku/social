# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import group.models
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0006_group_gtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='cover',
            field=stdimage.models.StdImageField(null=True, upload_to=group.models.group_cover_directory_path, blank=True),
        ),
    ]
