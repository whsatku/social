# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import User.models
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_auto_20151206_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='picture',
            field=stdimage.models.StdImageField(null=True, upload_to=User.models.user_picture_directory_path, blank=True),
        ),
    ]
