from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer
from newsfeed.models import Post, Comment


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
        read_only_fields = ('user')

class PostSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Post
        fields = ('id', 'user', 'text', 'date',
                  'target_type', 'target_id', 'target_object')
        read_only_fields = ('user',)


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'user', 'text', 'date')