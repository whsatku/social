from django.db import models
from django.contrib.auth.models import User
from social import settings


class Event(models.Model):
    name = models.CharField(max_length=25)
    start_date = models.DateTimeField(auto_now_add=False)
    end_date = models.DateTimeField(auto_now_add=False)
    description = models.CharField(max_length=200)
    # start_time = models.TimeField(auto_now_add=False)
    # end_time = models.TimeField(auto_now_add=False)

    def __unicode__(self):
        return "event : {}".format(self.name)


class EventMember(models.Model):
    event = models.ForeignKey(Event, default=0)
    user = models.ForeignKey(User, default=0)
    role = models.IntegerField()

    def __unicode__(self):
        return "event member : {}".format(self.user.username)
