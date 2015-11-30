from rest_framework import serializers
from models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


class EventMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = EventMember
        fields = ('user', 'role')


class EventSerializer(serializers.ModelSerializer):

    member_status = serializers.IntegerField(read_only=True, required=False)
    member_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'name', 'start_date', 'end_date', 'description',
                        'member_status', 'member_count')
