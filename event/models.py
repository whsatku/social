from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=25)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=250)


class EventMember(models.Model):
    event = models.ForeignKey(Event, default=0)
    user = models.ForeignKey(User, default=0)
    role = models.IntegerField()
