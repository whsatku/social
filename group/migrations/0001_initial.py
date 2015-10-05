# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=25)),
                ('type', models.IntegerField(default=0)),
                ('description', models.CharField(max_length=50)),
                ('long_description', models.CharField(max_length=200)),
                ('logo', models.CharField(max_length=25)),
                ('header', models.CharField(max_length=25)),
                ('permisssion', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group_Member',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('group_id', models.IntegerField(default=0)),
                ('user_id', models.IntegerField(default=0)),
                ('role', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
