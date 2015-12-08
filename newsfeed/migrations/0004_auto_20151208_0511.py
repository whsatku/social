# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import newsfeed.models


class Migration(migrations.Migration):

    dependencies = [
        ('newsfeed', '0003_comment_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='file',
            field=models.FileField(null=True, upload_to=newsfeed.models.comment_file_name),
        ),
    ]
