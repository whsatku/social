from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from group.serializers import GroupSerializer
from rest_framework.serializers import ModelSerializer
from newsfeed.models import Post, Comment
from User.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('picture', 'cover')


class UserSerializer(ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'profile')


class PostSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    datetime = serializers.ReadOnlyField()
    target_name = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ('id', 'user', 'text', 'datetime',
                  'target_type', 'target_id', 'target_name')


class GroupPostSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    target_type = serializers.HiddenField(default=ContentType.objects.get(model='group', app_label='group').id)
    target_id = serializers.HiddenField(default=1)
    datetime = serializers.ReadOnlyField()
    target_name = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ('id', 'user', 'text', 'datetime',
                  'target_type', 'target_id', 'target_name', 'pinned', 'allow_submission')


class EventPostSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    target_type = serializers.HiddenField(default=ContentType.objects.get(model='event').id)
    target_id = serializers.HiddenField(default=1)
    datetime = serializers.ReadOnlyField()
    target_name = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ('id', 'user', 'text', 'datetime',
                  'target_type', 'target_id', 'target_name', 'pinned', 'allow_submission')


class CommentSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    datetime = serializers.ReadOnlyField()
    file = serializers.FileField(read_only=True, use_url=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'user', 'text', 'datetime', 'file')
