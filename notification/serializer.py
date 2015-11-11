from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from models import Notification


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class UserNotificationSerializer(ModelSerializer):
    auto_created = True

    class Meta:
        model = User
        fields = ('id', 'username')


class NotificationSerializer(ModelSerializer):
    receiver = UserNotificationSerializer(read_only=True, many=True)
    readed = UserNotificationSerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True)
    datetime = serializers.ReadOnlyField(source='FORMAT')
    # link_type = serializers.HiddenField(default=13)

    class Meta:
        model = Notification
        fields = ('id', 'user', 'datetime',
                  'text', 'target_type', 'target_id',
                  'link_type', 'link_item', 'receiver', 'readed')


class UpdateNotificationSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    readed = UserNotificationSerializer(read_only=True, many=True)

    class Meta:
        model = Notification
        fields = ('id', 'user', 'readed')
