from django.db import models
from django.contrib.auth.models import User


GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
)

# Create your models here.1
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=5, choices=GENDER)
    faculty = models.CharField(max_length=30)
    major = models.CharField(max_length=30)
    types = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    # picture = StdImageField(null=True, blank=True, upload_to='images/profilepic',
    #                         variations={
    #                             'retina': (960, 960, True),
    #                             'normal': (240, 240, True),
    #                             'thumbnail': (160, 160, True)}
    #                         )
    # phone = models.CharField(max_length=20, blank=True)

    def __unicode__(self):
        return "{}'s profile".format(self.user.username)

    class Meta:
        db_table = 'youniversity_profile'