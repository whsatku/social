from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static

from rest_framework import serializers

from models import *
from friendship.models import Friend
from friendship.models import Follow


class UserProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ( 'picture',)


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfilePictureSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'profile')

class PictureField(serializers.Field):
    def to_representation(self, obj):
        if obj:
            return obj.url
        else:
            return static('assets/img/default.jpg')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    picture = PictureField(read_only=True)
    class Meta:
        model = UserProfile
        fields = ('user', 'firstname', 'lastname', 'birthday',
                  'gender', 'faculty', 'major', 'types',
                  'country', 'city', 'picture', 'cover', 'created')
        read_only_fields = ('picture', 'cover')

class UserCoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('cover',)

class FirstUserProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('user', 'faculty', 'country', 'created')


class FriendShipSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='from_user')

    class Meta:
        model = Friend
        fields = ('user', 'created')
