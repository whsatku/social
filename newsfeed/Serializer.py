from django.contrib.auth.models import User

from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer
from newsfeed.models import Post, Comment


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'text', 'date', 'target_type', 'target_id', 'target_object')


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'user', 'text', 'date')

