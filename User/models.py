from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount
from django.db.models.signals import post_save


GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
)

# Create your models here.1
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    firstname = models.CharField(max_length=30, null=True)
    lastname = models.CharField(max_length=30, null=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=5, choices=GENDER, null=True)
    faculty = models.CharField(max_length=30, null=True)
    major = models.CharField(max_length=30, null=True)
    types = models.CharField(max_length=30, null=True)
    country = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    created = models.BooleanField(default=False)
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


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create a matching profile whenever a user object is created."""
    if created:
        profile, new = UserProfile.objects.get_or_create(user=instance)
