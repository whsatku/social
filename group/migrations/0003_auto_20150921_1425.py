# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('group', '0002_auto_20150920_1117'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=50)),
                ('group_id', models.ForeignKey(default=0, to='group.Group')),
                ('user_id', models.ForeignKey(default=0, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Group_Member',
        ),
    ]
