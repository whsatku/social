from rest_framework import serializers
from models import *


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('user', 'birthday', 'gender', 'faculty', 'major', 'types')