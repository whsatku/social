from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from newsfeed.models import Post, Comment


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class PostSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    datetime = serializers.ReadOnlyField(source='FORMAT')

    class Meta:
        model = Post
        fields = ('id', 'user', 'text', 'datetime',
                  'target_type', 'target_id')
        # 'target_type', 'target_id', 'target_object')


class GroupPostSerializer(ModelSerializer):
    group_model_id = 15
    user = UserSerializer(read_only=True)
    target_type = serializers.HiddenField(default=group_model_id)
    target_id = serializers.HiddenField(default=1)
    datetime = serializers.ReadOnlyField(source='FORMAT')

    class Meta:
        model = Post
        fields = ('id', 'user', 'text', 'datetime',
                  'target_type', 'target_id')


class CommentSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    datetime = serializers.ReadOnlyField(source='FORMAT')

    class Meta:
        model = Comment
        fields = ('id', 'post', 'user', 'text', 'datetime')
