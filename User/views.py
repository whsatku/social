from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import NotAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from django.contrib.contenttypes.models import ContentType
from models import *
from serializers import *
from django.http import Http404
from rest_framework import status


class UserInformation (APIView):
    """This class is an API for getting user's user information

    Attribute:
            serializer_class: serializer for this class.

    """

    serializer_class = UserProfileSerializer

    def get_user(self, user_profile_id):
        """Get user from user profile's database.

        Args:
                user_profile_id: ID of user profile.

        Return:
                UserProfile object by ID.

        """
        try:
            return UserProfile.objects.get(id=user_profile_id)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, user_profile_id, format=None):
        """For client to get user profile's data from server.

        Args:
                request: Django Rest Framework request object.
                user_profile_id: ID of user profile.
                format: pattern for Web APIs.

        Return:
                UserProfile object by ID.

        """
        user_profile_object = self.get_user(user_profile_id)
        response = self.serializer_class(user_profile_object)
        return Response(response.data)

class FriendShipDetail(APIView):
    def get_user(self, user_profile_id):
        """Get user from user profile's database.

        Args:
                user_profile_id: ID of user profile.

        Return:
                UserProfile object by ID.

        """
        try:
            return UserProfile.objects.get(id=user_profile_id)
        except UserProfile.DoesNotExist:
            raise Http404

    # def get(self, request, user_profile_id, format=None):
    #     user_profile_object = self.get_user(user_profile_id)
    #     response = self.serializer_class(user_profile_object)
    #     return Response(response.data)


    def post(self, request, user_profile_id, other_user_id, format=None):
        user = self.get_user(user_profile_id)
        other_user = self.get_user(other_user_id)
        new_relationship = Friend.objects.add_friend(user, other_user)
        return Response(status=status.HTTP_201_CREATED)
