from django.contrib.auth.models import User
from rest_framework import serializers
from models import *
from newsfeed.serializer import UserSerializer
from friendship.models import Friend
from friendship.models import Follow


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('user', 'birthday', 'gender', 'faculty', 'major', 'types', 'country', 'city', 'created')


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
