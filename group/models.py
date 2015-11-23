from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class GroupCategory(models.Model):
    name = models.CharField(max_length=25)

    def __unicode__(self):
        return "category : {}".format(self.name)


class Group(models.Model):
    name = models.CharField(max_length=25)
    type = models.IntegerField(default=0)
    category = models.ForeignKey(GroupCategory, default=0)
    description = models.CharField(max_length=200)
    short_description = models.CharField(max_length=50)
    activities = models.CharField(max_length=200)
    logo = models.CharField(max_length=25)
    #logo_image = ImageField(upload_to=get_image_path, blank=True, null=True)
    header = models.CharField(max_length=25)
    #header_image = ImageField(upload_to=get_image_path, blank=True, null=True)
    permisssion = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return "group : {}".format(self.name)


class GroupMember(models.Model):
    group = models.ForeignKey(Group, default=0)
    user = models.ForeignKey(User, default=0)
    role = models.IntegerField()

    def create(self, new_group, new_user):
        self.create(new_group, new_user, 1)

    def __unicode__(self):
        return "{}:{}'s profile".format(self.user.username, self.group.name)
