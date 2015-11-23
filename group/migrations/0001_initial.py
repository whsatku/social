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
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=25)),
                ('type', models.IntegerField(default=0)),
                ('description', models.CharField(max_length=200)),
                ('short_description', models.CharField(max_length=50)),
                ('activities', models.CharField(max_length=200)),
                ('logo', models.CharField(max_length=25)),
                ('header', models.CharField(max_length=25)),
                ('permisssion', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='GroupCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.IntegerField()),
                ('group', models.ForeignKey(to='group.Group')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='category',
            field=models.ForeignKey(default=0, to='group.GroupCategory'),
        ),
    ]
