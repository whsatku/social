from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=25)
    type =  models.IntegerField(default=0)
    description = models.CharField(max_length=50)
    long_description = models.CharField(max_length=200)
    logo = models.CharField(max_length=25)
    #logo_image = ImageField(upload_to=get_image_path, blank=True, null=True)
    header = models.CharField(max_length=25)
    #header_image = ImageField(upload_to=get_image_path, blank=True, null=True)
    permisssion = models.IntegerField(default=0)

class GroupMember(models.Model):
    group_id = models.ForeignKey(Group, default=0)
    user_id = models.ForeignKey(User, default=0)
    role = models.IntegerField()
