from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.humanize.templatetags.humanize import naturaltime


class Post(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=2000)
    datetime = models.DateTimeField(auto_now_add=True)
    target_type = models.ForeignKey(ContentType)
    target_id = models.PositiveIntegerField(null=True)
    target_object = GenericForeignKey('target_type', 'target_id')
    allow_submission = models.BooleanField(default=False)
    pinned = models.BooleanField(default=False)

    def FORMAT(self):
        return naturaltime(self.datetime)

    def __unicode__(self):
        return "{}'s newsfeed (id={})".format(self.user.username, self.id)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
    text = models.CharField(max_length=2000)
    datetime = models.DateTimeField(auto_now_add=True)
    file = models.FileField(
        upload_to=lambda instance, filename: 'posts/{0}_{1}'.format(instance.id, filename),
        null=True
    )

    def __unicode__(self):
        return "{}'s comment (id={})".format(self.user.username, self.id)
