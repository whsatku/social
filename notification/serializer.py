from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from models import Notification


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class NotificationSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    datetime = serializers.ReadOnlyField(source='FORMAT')

    class Meta:
        model = Notification
        fields = ('id', 'user', 'datetime',
                  'message', 'target_type', 'target_id')
