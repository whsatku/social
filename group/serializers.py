from rest_framework import serializers
from models import *

class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = ('user_id', 'role')