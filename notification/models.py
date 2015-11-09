from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.humanize.templatetags.humanize import naturaltime


class Notification(models.Model):
    user = models.ForeignKey(User)
    datetime = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=2000)
    target_type = models.ForeignKey(ContentType)
    target_id = models.PositiveIntegerField(null=True)
    target_object = GenericForeignKey('target_type', 'target_id')

    def FORMAT(self):
        return naturaltime(self.datetime)

    def __unicode__(self):
        return "Notification (id={}) by {}".format(self.id, self.user.username)