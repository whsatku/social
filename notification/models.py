from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notificator')
    datetime = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=2000)
    receiver = models.ManyToManyField(User, through='UserNotification', blank=True, related_name='targets')
    readed = models.ManyToManyField(User, blank=True, related_name='readed')
    target_type = models.ForeignKey(ContentType, null=True, related_name='target_type')
    target_id = models.PositiveIntegerField(null=True)
    target_object = GenericForeignKey('target_type', 'target_id')
    link_type = models.ForeignKey(ContentType, related_name='link', null=True)
    link_item = models.CharField(max_length=2000, null=True)

    def __unicode__(self):
        return "Notification (id={}) by {}".format(self.id, self.user.username)


class UserNotification(models.Model):
    notification = models.ForeignKey(Notification)
    receiver = models.ForeignKey(User)
