from django.contrib.auth.models import User

from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
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


class TypeSerializer(ModelSerializer):
    class Meta:
        model = ContentType
        fields = ('id', 'model')


class NotificationSerializer(ModelSerializer):
    receiver = UserNotificationSerializer(read_only=True, many=True)
    readed = UserNotificationSerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True)
    datetime = serializers.ReadOnlyField()
    link_type = TypeSerializer(read_only=True)
    # link_item = serializers.DictField(child=serializers.CharField())

    class Meta:
        model = Notification
        fields = ('id', 'user', 'datetime',
                  'text', 'target_type', 'target_id',
                  'link_type', 'link_item', 'reference_detail',
                  'receiver', 'readed')


class GetNotificationSerializer(ModelSerializer):
    read = serializers.BooleanField()
    user = UserSerializer(read_only=True)
    datetime = serializers.ReadOnlyField()
    link_type = TypeSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ('id', 'user', 'datetime',
                  'text', 'target_type', 'target_id',
                  'link_type', 'link_item', 'reference_detail', 'read')


class UpdateNotificationSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    readed = UserNotificationSerializer(read_only=True, many=True)

    class Meta:
        model = Notification
        fields = ('id', 'user', 'readed')
