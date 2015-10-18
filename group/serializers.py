from rest_framework import serializers
from models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class GroupMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = GroupMember
        fields = ('user', 'role')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        app_label = "social_group"
        model = Group
        fields = ('name', 'description', 'short_description', 'activities', 'type')