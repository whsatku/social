from rest_framework import serializers
from models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class EventMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GroupMember
        fields = ('user', 'role')

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('name', 'start_date', 'end_date','description')


