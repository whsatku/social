from django.contrib.auth.models import User
from rest_framework import serializers

from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer
from newsfeed.models import Post, Comment


class PostSerializer(ModelSerializer):

    #user = serializers.SerializerMethodField('_user')

    # Use this method for the custom field
    def _user(self, obj):
        users = self.context['request'].user
        return users

    class Meta:
        model = Post
        fields = ('id', 'user','text', 'date', 'target_type', 'target_id', 'target_object')
        #read_only_fields = ('user',)


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'user', 'text', 'date')

