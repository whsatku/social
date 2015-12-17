from django.db import models
from django.contrib.auth.models import User
from stdimage.models import StdImageField

# Create your models here.

def group_cover_directory_path(instance, filename):
# file will be uploaded to media/coverpic/user_<id>/<filename>
    return 'groupcoverpic/group_{0}/{1}'.format(instance.id, filename)
    
class GroupCategory(models.Model):
    name = models.CharField(max_length=25)

    def __unicode__(self):
        return "category : {}".format(self.name)


class Group(models.Model):
    name = models.CharField(max_length=25)
    # type
    gtype = models.IntegerField(default=0)
    # privacy
    type = models.IntegerField()
    category = models.ForeignKey(GroupCategory, null=True)
    description = models.CharField(max_length=200)
    short_description = models.CharField(max_length=50)
    activities = models.CharField(max_length=200)
    permisssion = models.IntegerField(null=True)
    date = models.DateField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    cover = StdImageField(
        null=True, 
        blank=True,
        upload_to=group_cover_directory_path,
        variations={
            'normal': (945, 200, True)
        }
    )

    def __unicode__(self):
        return "group : {}".format(self.name)


class GroupMember(models.Model):
    group = models.ForeignKey(Group)
    user = models.ForeignKey(User)
    role = models.IntegerField()

    def create(self, new_group, new_user):
        self.create(new_group, new_user, 1)

    def __unicode__(self):
        return "{}:{}'s profile".format(self.user.username, self.group.name)
