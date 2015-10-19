# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('message', models.CharField(max_length=2000)),
                ('target_id', models.PositiveIntegerField()),
                ('target_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(default=0, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
