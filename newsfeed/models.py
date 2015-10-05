from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Post(models.Model):
    user = models.ForeignKey(User, default=0)
    text = models.CharField(max_length=2000)
    date = models.DateField(auto_now_add=True)
    target_type = models.ForeignKey(ContentType)
    target_id = models.PositiveIntegerField()
    target_object = GenericForeignKey('target_type', 'target_id')

    def __unicode__(self):
        return "{}'s newsfeed (id={})".format(self.user.username, self.id)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
    text = models.CharField(max_length=2000)
    date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return "{}'s comment (id={})".format(self.user.username, self.id)
