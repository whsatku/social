from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Post(models.Model):
    user = models.ForeignKey(User, default=0)
    text = models.CharField(max_length=2000)
    date = models.DateField()
    target_type = models.ForeignKey(ContentType)
    target_id = models.PositiveIntegerField()
    target_object = GenericForeignKey('target_type', 'target_id')

    def __unicode__(self):
        return "{}'s newsfeed".format(self.user.username)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
    text = models.CharField(max_length=2000)
    date = models.DateField()

    def __unicode__(self):
        return "{}'s comment".format(self.user.username)
