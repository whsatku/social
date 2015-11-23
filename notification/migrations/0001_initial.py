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
                ('text', models.CharField(max_length=2000)),
                ('target_id', models.PositiveIntegerField(null=True)),
                ('link_item', models.CharField(max_length=2000, null=True)),
                ('reference_detail', models.CharField(max_length=2000, null=True)),
                ('link_type', models.ForeignKey(related_name='link', to='contenttypes.ContentType', null=True)),
                ('readed', models.ManyToManyField(related_name='readed', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notification', models.ForeignKey(to='notification.Notification')),
                ('receiver', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='notification',
            name='receiver',
            field=models.ManyToManyField(related_name='targets', through='notification.UserNotification', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='target_type',
            field=models.ForeignKey(related_name='target_type', to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(related_name='notificator', to=settings.AUTH_USER_MODEL),
        ),
    ]
