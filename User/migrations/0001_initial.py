# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('birthday', models.DateField(null=True, blank=True)),
                ('gender', models.CharField(max_length=5, null=True, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('faculty', models.CharField(max_length=30, null=True)),
                ('major', models.CharField(max_length=30, null=True)),
                ('types', models.CharField(max_length=30, null=True)),
                ('country', models.CharField(max_length=50, null=True)),
                ('city', models.CharField(max_length=50, null=True)),
                ('created', models.BooleanField(default=False)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'youniversity_profile',
            },
        ),
    ]
